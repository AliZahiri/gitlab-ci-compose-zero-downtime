# Define health endpoint contract

<!-- daily-pr-task: health-endpoint-contract -->

Health checks should represent readiness, not only process liveness. The deployment script promotes a color only after the container reports ready.

A useful readiness endpoint should verify:

- application process is accepting requests
- critical dependencies are reachable
- migrations required by the running version are applied
- the app can serve a minimal real request path

## Portfolio Value

Strengthens the health-check-gated deployment claim with an explicit contract.

## Validation

Review the markdown file and confirm the readiness criteria are concrete.
