# Add deployment freeze evidence gate

<!-- daily-pr-task: deployment-freeze-evidence-gate -->

This offline contract validates fresh, timezone-aware freeze evidence. Standard deployment is blocked during an active freeze. Emergency deployment requires an approval reference, approver, and recovery reason; it does not bypass health, artifact, or rollback gates.

## Portfolio Value

Makes deployment freeze and emergency exception handling auditable alongside health-gated promotion.

## Validation

Run python3 -m unittest discover -s tests. Tests cover standard clearance, freeze blocking, an approved emergency path, stale evidence, and invalid policy or clock values.
