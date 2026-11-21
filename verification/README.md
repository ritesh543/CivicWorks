# Verification

| Check | Observed result | Evidence |
| --- | --- | --- |
| GenLayer Direct Mode | 24 tests passed across ten contracts. Includes alternative leader decisions, blocked calls and allowed state transitions. | [Test output](direct-tests.txt), [JUnit report](direct-tests.xml) |
| StudioNet deployments | Ten finalized transactions with successful constructors. Contract code matched all ten local SHA-256 digests. | [Explorer receipts](../DEPLOYMENTS.md), [Deployment records](../deployment_info.json) |
| Public reads | Each new instance returned zero records. NoticeClock returned 1,440 as its immutable minimum lead time. | [Live verification output](studionet-verification.txt) |
| StudioNet RPC simulations | Four initial write methods returned successfully in simulation. The live record count stayed the same before and after each run. | [Simulation records](studionet-simulations.json) |

The RPC observations are dated 21 November 2026. Direct Mode uses mocked model and web evidence to test both the leader and validator code. RPC simulations exercise individual examples without committing a transaction. The deployed transactions in this release are the ten constructors.
