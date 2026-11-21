# Reusing a consensus pattern

Each Python source bundles its own helpers so it can deploy in Studio as a single file. The small exact-result validator in [AccessPath](../contracts/access_path.py) independently reproduces a closed vocabulary result. It compares all consequential fields and accepts a successful return only.

[MinutesCommitment](../contracts/minutes_commitment.py) shows how to audit a selected source line against fixed inputs. Give the validator the full minutes, the leader's line number, and the exact claim. Store the original matching text with the decision.
