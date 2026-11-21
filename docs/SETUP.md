# Setup

## Open a deployed contract in Studio

1. Open [GenLayer Studio](https://studio.genlayer.com).
2. Copy the address for the desired contract from [DEPLOYMENTS.md](../DEPLOYMENTS.md).
3. Use the import-by-address control. Run `count()` to see the number of records.
4. Select any test account to start a new workflow. The wallet that creates the record controls its authorized updates.

For a new deployment in the Studio editor, load one file from `contracts/`. Enter `1440` for the default demo deployment of NoticeClock. The other nine constructors take zero arguments.

## Run local tests

Use Python 3.12 and the dependencies listed in [requirements-dev.txt](../requirements-dev.txt).

```sh
python3.12 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

Direct Mode downloads the GenVM Python SDK on first use. LLM and web responses in the direct suite come from test fixtures so each test can check the precise state transitions. Alternative leader results in these tests exercise the contract validator as well as the leader.

## Redeploy from a dedicated test wallet

Use Node.js 22 or newer. The script checks the StudioNet chain ID 61999 before signing. Create a local `.env` using `.env.example` and supply your own test wallet key for `STUDIONET_PRIVATE_KEY`.

```sh
npm ci
node --env-file=.env deploy/studionet.mjs submit
node deploy/studionet.mjs wait
```

The commands maintain `deployments.local.json` and keep the original batch journal while the current deployed contracts are tracked in `deployment_info.json`. If a submission becomes uncertain, the journal prevents guessing that it is safe to send the transaction again. Compare the recorded sender and the Studio explorer history before reconciling that entry. When a recorded transaction hash exists, a repeated `submit` uses it and skips another broadcast for that contract.

To verify the shipped deployment independently, run `npm run verify:live`. This checks finalized receipts, on-chain source hashes and live views using the public RPC. StudioNet is a shared development network whose state can be reset.

## Try the examples

[Example scenarios](../examples/scenarios.json) list the public methods, arguments, and expected observations for all ten contracts. In those examples, a `result` value stands for the result returned by the named earlier write. Replace a `scenario` object with a unique reference string. In HandoffCondition, use the recipient wallet's address for the `account` value, then use that wallet to inspect the offer.

To run four examples in simulation through the public StudioNet RPC, use this command after `npm ci`.

```sh
node deploy/simulate.mjs
```

The simulator returns the execution result and checks that the persistent record count stays the same. A signer is unnecessary.
