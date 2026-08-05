# Add release dependency health contract

<!-- daily-pr-task: release-dependency-health-contract -->

Docker Compose starts dependencies in declaration order unless a dependency condition is made explicit. This offline gate evaluates supplied Compose service metadata before a blue-green promotion: it requires the promoted service to expose a health check, rejects service_started as a promotion dependency condition, detects missing or self-referential dependencies, and rejects dependency cycles. It does not contact Docker or mutate a deployment.

## Portfolio Value

Makes Compose startup ordering a reviewable promotion contract so the new color is not exposed before its critical dependencies have completed or become healthy.

## Validation

Run `python3 -m unittest discover -s tests` and confirm health-gated dependencies pass while missing health checks, service_started conditions, unknown or self dependencies, cycles, and invalid promoted-service policy fail.
