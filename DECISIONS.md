# Design decisions

## Bind the result that changes state

Nine contracts have a validator independently repeat the task and compare the normalized result exactly. For instance, an AccessPath validator must reproduce each of the three features, and a MeterContinuity validator must agree whether a lower reading reflects a wrap or replacement. These values lead to different records or arithmetic. The direct tests pass alternative leader outputs to the actual validator functions and verify rejection.

MinutesCommitment uses a different method because two paragraphs could validly support the same decision. The leader chooses a line index. Each validator reviews that exact line against the same full claim and checks the minutes for reversal. The recorded quote is selected from the stored minutes by deterministic indexing.

## Separate consent and arithmetic from model output

The model returns short categories or a line number. Range checks, exact units, capacity accounting, participant authorizations and permitted transitions run in deterministic code. Several methods skip model work completely. Adjacent roadwork windows have zero overlap, and normal meter increments can be checked using the displayed numbers.

## Evidence inputs and roles

Most contracts assess submitted public text. A signed input identifies its submitting wallet. Integrators still need to establish which wallets represent the venue, board or operator and where the material came from. For NoticeClock, the UTC minutes and date label are caller assertions. For OpenFieldMap, the column's declared source unit fixes the conversion. GenLayer call data is public, including text whose persistent record stores only a digest.

PublicFeedPulse composes two live reads. Distinct hostnames provide two observations, with no guarantee of independent organizational control or authenticity of their contents. It limits each input sent to the model to the leading 3,800 characters, and the retained scan stores the verdicts. The allowlist covers a small set of government domains and the two IANA example domains used for the live demonstration. Confirmations are about consecutive transactions.

## Deployment scope

Each instance is permissionless at entry. Rights arise from creating a record, proposal, channel or watch, or being named as the handoff recipient. Therefore, users can start their own flows on the published instances regardless of which test wallet deployed them. The deployments use a dedicated StudioNet signing wallet and the HandoffCondition smoke scenario uses a second signer. The archive contains public evidence and reproducible commands.

## Reference

The catalog layout was reviewed against Penumbra at `2cc5c14049433e419b4fd0d487fbffbe85daf8b6`. The contract workflows and source were written for CivicWorks. [Penumbra at the reviewed revision](https://github.com/luch91/penumbra/tree/2cc5c14049433e419b4fd0d487fbffbe85daf8b6)
