# Add Compose health endpoint contract gate

<!-- daily-pr-task: compose-health-endpoint-contract-gate -->

A container health command and a public promotion check must observe the same explicit contract. This offline gate validates declared service health endpoint metadata: an absolute health path, a success status, a bounded timeout, and an explicit authentication-free probe designation. It validates configuration only and does not make network calls.

## Portfolio Value

Aligns readiness and promotion checks around an explicit, bounded health endpoint contract so deployments do not rely on undocumented probe behavior.

## Validation

Run python3 -m unittest discover -s tests and confirm only unique, authentication-free absolute health endpoints with HTTP 200 and bounded timeouts pass.
