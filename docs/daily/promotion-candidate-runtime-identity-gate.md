# Add promotion candidate runtime identity gate

<!-- daily-pr-task: promotion-candidate-runtime-identity-gate -->

Before traffic switches, observed candidate runtime evidence should match the release plan. This offline gate compares immutable image digests and configuration fingerprints, requires the candidate container to be running, and records a timezone-aware observation.

## Portfolio Value

Connects immutable release intent to the container and configuration actually running before Nginx promotion.

## Validation

Run python3 -m unittest discover -s tests and confirm digest drift, configuration drift, stopped candidates, and naive observations fail.
