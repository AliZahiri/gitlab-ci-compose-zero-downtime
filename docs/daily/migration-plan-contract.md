# Add migration plan safety contract

<!-- daily-pr-task: migration-plan-contract -->

Blue-green traffic switching cannot make a destructive database migration safe. This contract validates ordered expand/backfill/contract phases and requires evidence that the backward-compatibility window completed and rollback was tested before a contract step can run. It turns the existing migration guidance into an executable release gate.

## Portfolio Value

Converts migration compatibility assumptions into a deterministic promotion control for safer Compose blue-green releases.

## Validation

Run `python3 -m unittest discover -s tests` and confirm contract phases fail without an earlier expand phase plus compatibility and rollback evidence.
