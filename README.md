# CivicWorks

CivicWorks is a catalog of ten GenLayer Intelligent Contracts for facilities and public-service workflows. Each contract runs on its own and has a focused test module. A facilities team can use one contract to compare street closures, another to reconcile equipment handoffs, and another to certify an action from meeting minutes.

| Contract | Workflow | State rule |
| --- | --- | --- |
| [AccessPath](contracts/access_path.py) | Build an accessibility card for a specific entrance and route | Each feature has its own conclusion. Repeating the same evidence under the same signer returns the original card. |
| [WorksConflict](contracts/works_conflict.py) | Identify clashes between two roadworks schedules | An exact time overlap and a confirmed shared corridor are required for a conflict. |
| [RepairMerge](contracts/repair_merge.py) | Link duplicate facilities work orders | A review can link tickets only for the same operator and site. The originals stay readable. |
| [NoticeClock](contracts/notice_clock.py) | Check the contents and lead time of a service notice | Both the content check and the minute threshold must pass. |
| [OpenFieldMap](contracts/open_field_map.py) | Map a public dataset column to a canonical measurement | Only the publisher can activate a matching proposal. Each feed revision has one binding per column. |
| [HandoffCondition](contracts/handoff_condition.py) | Compare declared and observed equipment condition | The recipient inspects. A condition exception stays open until the sender resolves it. |
| [DonationAllocation](contracts/donation_allocation.py) | Reserve reuse capacity for eligible lots | Capacity moves between available, reserved, and distributed quantities. Only the organizer can allocate it. |
| [MinutesCommitment](contracts/minutes_commitment.py) | Cite the minutes behind a claimed board decision | Validators verify the selected paragraph against the full action, assignee, and deadline. |
| [MeterContinuity](contracts/meter_continuity.py) | Reconcile backward readings after rollover or meter replacement | A rollover must fit the configured numeric limit. A replacement begins a new segment with zero credited increment. |
| [PublicFeedPulse](contracts/public_feed_pulse.py) | Check whether two public pages list or pause a service | Two consecutive matching observations are required. A conflicting or unavailable source returns the watch to unconfirmed. |

[StudioNet addresses and explorer receipts](DEPLOYMENTS.md) are included with the source hashes in [deployment_info.json](deployment_info.json). [Verification evidence](verification/README.md) records the successful deployments, live source checks, and local contract tests.

## Run and inspect

The local suite uses Python 3.12 and GenLayer Direct Mode. It exercises the published contract methods with controlled LLM and web inputs, including cases where validators reach different outcomes.

```sh
python3.12 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

To check the deployed versions using the public RPC, install the JavaScript SDK and run the read-only verifier.

```sh
npm ci
npm run verify:live
```

[Setup](docs/SETUP.md) covers GenLayer Studio, deployments from a new test wallet, and live smoke scenarios. [Contract specifications](CONTRACTS.md) list the methods and expected transitions. [Design decisions](DECISIONS.md) describe what validators check and which inputs remain caller attestations.

The layout follows the [Penumbra repository](https://github.com/luch91/penumbra), with standalone sources in `contracts/`, one test module per contract in `tests/`, and the deployment and design evidence alongside them.
