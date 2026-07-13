# Add rollback readiness check

<!-- daily-pr-task: rollback-readiness-check -->

A zero-downtime rollback is only possible when the previous color is still healthy and the proxy can switch back safely. This check turns that operational assumption into an explicit release gate.

## Portfolio Value

Makes rollback claims concrete by validating health and proxy readiness before release traffic moves.

## Validation

Run `python3 -m unittest discover -s tests` and confirm missing rollback gates are visible.
