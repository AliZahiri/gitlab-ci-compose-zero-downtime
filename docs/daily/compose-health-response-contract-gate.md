# Add Compose health response contract gate

<!-- daily-pr-task: compose-health-response-contract-gate -->

A 200 status alone can be misleading when a health endpoint returns an empty or unstructured response. This offline gate validates an explicit response contract for promotion probes: a service name, expected status, bounded content type, and a declared required JSON field. It validates metadata only and does not make HTTP calls.

## Portfolio Value

Prevents traffic promotion from accepting weak or undocumented health responses by making successful probe semantics reviewable.

## Validation

Run python3 -m unittest discover -s tests and confirm unique JSON/200 health contracts with one required field pass while weak response contracts fail.
