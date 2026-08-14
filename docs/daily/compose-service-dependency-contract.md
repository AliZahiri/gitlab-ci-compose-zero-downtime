# Add Compose service dependency contract

<!-- daily-pr-task: compose-service-dependency-contract -->

Blue-green promotion requires dependencies to be explicitly health-gated. This offline contract checks declared Compose service metadata for unique service names and requires critical dependencies to use the Compose service_healthy condition with restart propagation. It validates a supplied plan; it does not deploy containers.

## Portfolio Value

Makes Compose dependency behavior reviewable before a promotion, avoiding an unsupported zero-downtime claim when a critical backend is merely started rather than healthy.

## Validation

Run `python3 -m unittest discover -s tests` and confirm health-gated dependencies pass while empty plans, duplicate names, malformed dependencies, non-health conditions, and missing restart propagation fail.
