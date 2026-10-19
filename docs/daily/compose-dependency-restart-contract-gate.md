# Add Compose dependency restart contract gate

<!-- daily-pr-task: compose-dependency-restart-contract-gate -->

A blue-green candidate can pass its initial health check and still remain unavailable after an operator restarts a dependency. This offline gate validates explicit long-form Docker Compose dependency contracts: referenced services must exist, dependencies must be health-gated, required, and configured to restart with an explicitly restarted dependency. It validates declared Compose metadata only; it does not start containers.

## Portfolio Value

Protects blue-green promotion from dependency restart surprises by making health, restart propagation, and required-dependency assumptions reviewable before deployment.

## Validation

Run python3 -m unittest discover -s tests and confirm only declared, health-gated, required dependencies with restart propagation pass.
