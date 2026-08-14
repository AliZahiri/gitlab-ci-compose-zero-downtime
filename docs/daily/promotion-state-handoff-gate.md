# Add promotion state handoff gate

<!-- daily-pr-task: promotion-state-handoff-gate -->

A traffic switch is recoverable only when both colors and rollback state are recorded. This offline gate validates a promotion handoff record: distinct active and standby colors, immutable candidate and rollback artifact digests, passing candidate health, and a captured rollback readiness decision.

## Portfolio Value

Connects traffic promotion to rollback evidence and immutable artifacts, making the deployment story precise and operationally credible.

## Validation

Run `python3 -m unittest discover -s tests` and confirm recoverable handoffs pass while same colors, mutable digests, unhealthy candidates, and absent rollback readiness fail.
