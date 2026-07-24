# Add promotion readiness gate

<!-- daily-pr-task: promotion-readiness-gate -->

Traffic promotion should require a recoverable checkpoint, a satisfied consecutive-health window, and a release health budget in one decision. This gate composes the existing policies and returns explicit failure names before the Nginx switch is attempted.

## Portfolio Value

Connects health, rollback, artifact, and proxy invariants into one auditable promotion decision.

## Validation

Run `python3 -m unittest discover -s tests` and confirm checkpoint, health-window, and release-budget failures all block promotion.
