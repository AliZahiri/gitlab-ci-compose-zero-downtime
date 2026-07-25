# Add promotion evidence contract

<!-- daily-pr-task: promotion-evidence-contract -->

A blue/green promotion should leave one machine-readable decision record rather than relying on disconnected log lines. This contract requires release identity, distinct deployment colors, a minimum number of successful health samples, proxy validation, smoke-test success, traffic-switch confirmation, and rollback readiness. It validates evidence metadata only and does not claim zero downtime by itself.

## Portfolio Value

Creates a reviewable promotion record spanning health, proxy, smoke, traffic, and rollback signals without overstating zero-downtime guarantees.

## Validation

Run `python3 -m unittest discover -s tests` and confirm complete evidence passes while missing identity, invalid colors, insufficient health samples, failed proxy/smoke/switch confirmation, or absent rollback readiness fail together.
