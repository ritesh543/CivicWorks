import assert from "node:assert/strict";
import { resolve } from "node:path";
import { chainId, connect, readJson, root, saveJson, shortError } from "./studionet.mjs";

const output = process.argv[2] ? resolve(process.argv[2]) : undefined;
const info = readJson(resolve(root, "deployment_info.json"));
const scenarios = readJson(resolve(root, "examples/scenarios.json"));
const names = ["AccessPath", "WorksConflict", "NoticeClock", "OpenFieldMap"];

async function simulate() {
  assert.equal(info.chain_id, chainId);
  const { client } = await connect();
  const report = { network: "studionet", chain_id: chainId, mode: "rpc_simulation", cases: {} };
  for (const name of names) {
    const { address, status } = info.deployments[name];
    assert.equal(status, "FINALIZED");
    const step = scenarios[name].writes[0];
    const args = step.args.map(arg => arg?.scenario ? "simulation-" + arg.scenario : arg);
    const entry = { address, method: step.method };
    try {
      const countBefore = await client.readContract({ address, functionName: "count" });
      const result = await client.simulateWriteContract({ address, functionName: step.method, args });
      const countAfter = await client.readContract({ address, functionName: "count" });
      entry.return_value = typeof result === "bigint" ? Number(result) : result;
      entry.count_before = countBefore;
      entry.count_after = countAfter;
      assert.equal(entry.return_value, countBefore);
      assert.equal(countAfter, countBefore);
      entry.status = "PASS";
    } catch (error) {
      entry.status = "UNVERIFIED";
      entry.error = shortError(error);
    }
    report.cases[name] = entry;
    console.log(name, entry.status, entry.error ?? "");
  }
  report.checked_at = new Date().toISOString();
  report.passed = Object.values(report.cases).filter(entry => entry.status === "PASS").length;
  if (output) saveJson(output, report);
  if (report.passed !== names.length) process.exitCode = 1;
}

simulate().catch(error => {
  console.error(shortError(error));
  process.exitCode = 1;
});
