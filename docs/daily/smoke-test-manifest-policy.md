# Add smoke test manifest policy

<!-- daily-pr-task: smoke-test-manifest-policy -->

Smoke test manifest policy should make post-start validation explicit before promoting a new color. Each check should declare a name, endpoint, expected status, and timeout.

Policy checks:

- at least one smoke check
- every check has a name
- every check has a path
- timeout is positive

## Portfolio Value

Shows zero-downtime promotion is gated by explicit post-start smoke checks.

## Validation

Run the unit test and confirm smoke manifests require named checks and timeouts.
