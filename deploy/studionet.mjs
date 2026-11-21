import { createHash } from "node:crypto";
import { closeSync, existsSync, openSync, readFileSync, renameSync, unlinkSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";
import { setTimeout as delay } from "node:timers/promises";
import { fileURLToPath, pathToFileURL } from "node:url";
import { parseArgs } from "node:util";
import { createAccount, createClient } from "genlayer-js";
import { studionet } from "genlayer-js/chains";

export const root = fileURLToPath(new URL("../", import.meta.url));
export const chainId = 61999;
export const rpcUrl = "https://studio.genlayer.com/api";
export const explorer = "https://explorer-studio.genlayer.com";

const manifest = readJson(resolve(root, "deploy/manifest.json"));

export function readJson(path) {
  return JSON.parse(readFileSync(path, "utf8"));
}

export function saveJson(path, value) {
  const temporary = path + ".tmp";
  writeFileSync(temporary, JSON.stringify(value, null, 2) + "\n", { mode: 0o600 });
  renameSync(temporary, path);
}

export function shortError(error) {
  return (error.shortMessage ?? error.message ?? String(error)).split("\n", 1)[0];
}

export async function connect(privateKey) {
  const account = privateKey ? createAccount(privateKey) : undefined;
  const client = createClient({ chain: { ...studionet }, endpoint: rpcUrl, account });
  const id = await client.getChainId();
  if (id !== chainId) throw new Error(`Expected Studionet ${chainId}, received chain ${id}`);
  return { client, account };
}

export async function transaction(client, hash) {
  const raw = await client.request({ method: "eth_getTransactionByHash", params: [hash] });
  if (!raw) return null;
  const leaders = raw.consensus_data?.leader_receipt;
  const leader = Array.isArray(leaders) ? leaders[0] : leaders;
  const votes = Object.values(raw.consensus_data?.votes ?? {});
  return {
    status: raw.status,
    consensus_result: raw.result_name,
    execution_result: leader?.execution_result,
    agreeing_validators: votes.filter(vote => vote === "agree").length,
    configured_validators: raw.num_of_initial_validators,
    address: raw.data?.contract_address ?? raw.to_address,
    sender: raw.from_address,
    transaction_type: raw.type,
  };
}

export const sha256 = value => createHash("sha256").update(value).digest("hex");

function journal(deployer) {
  return { network: "studionet", chain_id: chainId, rpc_url: rpcUrl, explorer, deployer, deployments: {} };
}

function sourceFor(spec, previous) {
  const source = readFileSync(resolve(root, spec.file));
  const sourceDigest = sha256(source);
  if (previous && (previous.source_sha256 !== sourceDigest
      || JSON.stringify(previous.constructor_args) !== JSON.stringify(spec.args))) {
    throw new Error(`Source or arguments changed for ${spec.name}. Use a fresh journal for a new deployment.`);
  }
  return { source, sourceDigest };
}

async function submit(client, account, state, path, specs) {
  for (const spec of specs) {
    const previous = state.deployments[spec.name];
    const { source, sourceDigest } = sourceFor(spec, previous);
    if (previous?.transaction_hash) continue;
    if (previous) {
      throw new Error(`Submission for ${spec.name} needs reconciliation before broadcasting it again.`);
    }
    const schema = await client.getContractSchemaForCode(new Uint8Array(source));
    if (!schema?.methods?.count?.readonly || schema.ctor?.params.length !== spec.args.length) {
      throw new Error(`Unexpected contract schema for ${spec.name}`);
    }
    const entry = {
      file: spec.file,
      constructor_args: spec.args,
      source_sha256: sourceDigest,
      status: "SUBMITTING",
    };
    state.deployments[spec.name] = entry;
    saveJson(path, state);

    try {
      entry.transaction_hash = await client.deployContract({
        code: new Uint8Array(source), args: spec.args, leaderOnly: false,
      });
    } catch (error) {
      entry.status = "SUBMISSION_UNCERTAIN";
      entry.last_error = shortError(error);
      saveJson(path, state);
      throw new Error(`${spec.name} submission needs reconciliation: ${entry.last_error}`);
    }
    entry.status = "SUBMITTED";
    entry.submitted_at = new Date().toISOString();
    entry.transaction_url = `${explorer}/tx/${entry.transaction_hash}`;
    saveJson(path, state);
    console.log(`${spec.name} submitted by ${account.address} ${entry.transaction_hash}`);
  }
}

async function observe(client, state, spec, verifyFresh) {
  const entry = state.deployments[spec.name];
  if (!entry?.transaction_hash) return false;
  sourceFor(spec, entry);
  const observed = await transaction(client, entry.transaction_hash);
  if (!observed) return false;
  if (observed.sender?.toLowerCase() !== state.deployer.toLowerCase() || observed.transaction_type !== 1) {
    throw new Error(`Deployment receipt identity mismatch for ${spec.name}`);
  }
  if (entry.status !== observed.status) console.log(`${spec.name} ${observed.status}`);
  entry.status = observed.status;
  entry.execution_result = observed.execution_result;
  entry.consensus_result = observed.consensus_result;
  entry.agreeing_validators = observed.agreeing_validators;
  entry.configured_validators = observed.configured_validators;
  entry.transaction_url = `${explorer}/tx/${entry.transaction_hash}`;

  const decided = observed.status === "FINALIZED" || observed.status === "ACCEPTED";
  if (!decided || observed.execution_result !== "SUCCESS" || observed.consensus_result !== "MAJORITY_AGREE") return false;
  if (!entry.source_verified || verifyFresh || entry.address !== observed.address) {
    if (!/^0x[0-9a-f]{40}$/i.test(observed.address ?? "")) {
      throw new Error(`No usable contract address for ${spec.name}`);
    }
    const source = await client.getContractCode(observed.address);
    if (sha256(source) !== entry.source_sha256) {
      throw new Error(`On-chain source hash differs for ${spec.name}`);
    }
    const count = await client.readContract({ address: observed.address, functionName: "count" });
    if (!Number.isSafeInteger(count) || count < 0) throw new Error(`Invalid count for ${spec.name}`);
    entry.first_verified_count ??= count;
    entry.latest_verified_count = count;
    if (spec.name === "NoticeClock") {
      const threshold = await client.readContract({ address: observed.address, functionName: "minimum_lead" });
      if (threshold !== spec.args[0]) throw new Error("NoticeClock constructor value differs");
      entry.minimum_lead_verified = threshold;
    }
    entry.address = observed.address;
    entry.explorer_url = `${explorer}/address/${entry.address}`;
    entry.source_verified = true;
  }
  return observed.status === "FINALIZED";
}

async function monitor(client, state, path, specs, options, writeState) {
  const deadline = Date.now() + options.timeout * 1000;
  const pending = new Set(specs);
  do {
    const remaining = [...pending];
    // Limit concurrent calls against the shared Studio service.
    for (let index = 0; index < remaining.length; index += 3) {
      const group = remaining.slice(index, index + 3);
      const results = await Promise.allSettled(group.map(spec => observe(client, state, spec, !writeState)));
      for (let offset = 0; offset < group.length; offset++) {
        const result = results[offset];
        const spec = group[offset];
        if (result.status === "rejected") console.error(`${spec.name} ${shortError(result.reason)}`);
        else if (result.value) pending.delete(spec);
      }
      if (writeState) saveJson(path, state);
    }
    console.log(`${specs.length - pending.size}/${specs.length} finalized with verified source and contract reads`);
    if (pending.size === 0) return true;
    for (const spec of pending) {
      const entry = state.deployments[spec.name];
      if (entry?.status === "FINALIZED" && (entry.execution_result !== "SUCCESS" || entry.consensus_result !== "MAJORITY_AGREE")) {
        throw new Error(`Finalized constructor failed for ${spec.name} ${entry.transaction_hash}`);
      }
    }
    if (!options.wait || Date.now() >= deadline) return false;
    await delay(Math.min(12000, Math.max(0, deadline - Date.now())));
  } while (Date.now() <= deadline);
  return false;
}

async function main() {
  const { positionals: [command], values } = parseArgs({
    allowPositionals: true,
    options: { state: { type: "string" }, only: { type: "string" }, timeout: { type: "string" } },
  });
  if (!["submit", "poll", "wait", "verify"].includes(command)) {
    throw new Error("Usage: node deploy/studionet.mjs submit|poll|wait|verify [--state FILE] [--only CONTRACT] [--timeout SECONDS]");
  }
  const timeout = Number(values.timeout ?? (command === "verify" ? "75" : "420"));
  if (!Number.isSafeInteger(timeout) || timeout < 1 || timeout > 7200) throw new Error("Invalid timeout");
  const statePath = values.state ? resolve(values.state) : resolve(
    root, command === "verify" ? "deployment_info.json" : "deployments.local.json",
  );
  const specs = values.only ? manifest.filter(spec => spec.name === values.only) : manifest;
  if (!specs.length) throw new Error("Unknown contract name");
  const privateKey = command === "submit" ? process.env.STUDIONET_PRIVATE_KEY : undefined;
  if (command === "submit" && !privateKey) throw new Error("Set STUDIONET_PRIVATE_KEY for deployment");
  if (command !== "submit" && !existsSync(statePath)) throw new Error("Deployment journal is missing");

  const writeState = command !== "verify";
  const lock = writeState ? openSync(statePath + ".lock", "wx", 0o600) : undefined;
  try {
    const { client, account } = await connect(privateKey);
    const state = existsSync(statePath) ? readJson(statePath) : journal(account.address);
    if (state.network !== "studionet" || state.chain_id !== chainId || state.rpc_url !== rpcUrl) {
      throw new Error("Deployment journal is for a different network");
    }
    if (command === "submit") {
      if (state.deployer.toLowerCase() !== account.address.toLowerCase()) {
        throw new Error("Use the same test wallet to resume this journal");
      }
      await submit(client, account, state, statePath, specs);
    } else {
      const success = await monitor(client, state, statePath, specs, {
        wait: command !== "poll", timeout,
      }, writeState);
      if (!success) process.exitCode = 1;
    }
  } finally {
    if (lock !== undefined) {
      closeSync(lock);
      unlinkSync(statePath + ".lock");
    }
  }
}

if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  main().catch(error => {
    console.error(shortError(error));
    process.exitCode = 1;
  });
}
