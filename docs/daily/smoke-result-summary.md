# Add smoke result summary helper

<!-- daily-pr-task: smoke-result-summary -->

Smoke tests should leave a compact summary that can be attached to CI logs or release notes. A summary helps operators see which endpoint failed, how long checks took, and whether rollback should be considered.

Useful fields:

- check name
- target URL
- HTTP status
- duration in milliseconds
- pass/fail outcome

## Portfolio Value

Improves release observability around smoke tests and rollback decisions.

## Validation

Run `python3 -m unittest discover -s tests` and confirm smoke summaries mark slow or failing checks as failed.
