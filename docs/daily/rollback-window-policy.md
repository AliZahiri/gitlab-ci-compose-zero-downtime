# Add rollback window policy

<!-- daily-pr-task: rollback-window-policy -->

Rollback window policy should keep the old color available after promotion until smoke checks and observation complete. This makes compose-based deploys safer under failure.

Policy fields:

- keep-old-color seconds
- smoke-check seconds
- minimum observation seconds
- cleanup allowed flag

## Portfolio Value

Shows failed promotions keep the previous color available long enough for fast recovery.

## Validation

Run the unit test and confirm rollback windows preserve old color availability.
