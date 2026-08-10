# Add rollback command contract gate

<!-- daily-pr-task: rollback-command-contract -->

A rollback plan is only useful when it is executable without reconstructing deployment state under pressure. This offline gate validates a declared rollback command contract: the command is non-empty, references an immutable image digest, targets a known color, and has an explicit verification command. It evaluates supplied metadata only and never executes shell commands.

## Portfolio Value

Strengthens rollback readiness by requiring reviewable immutable deployment and verification intent before a failed promotion needs recovery.

## Validation

Run `python3 -m unittest discover -s tests` and confirm immutable, known, verified rollback contracts pass while mutable image tags, unknown colors, missing verification, and invalid policy inputs fail.
