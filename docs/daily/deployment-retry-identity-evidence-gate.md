# Add deployment retry identity evidence gate

<!-- daily-pr-task: deployment-retry-identity-evidence-gate -->

A restarted blue/green deployment must resume the same immutable release intent instead of silently changing image, environment, target color, or checkpoint history. This offline gate validates a bounded sequence of retry attempts, stable deployment identity, immutable image digest, unique attempt IDs, timezone-aware ordering, and monotonic checkpoints before a retry is allowed to continue.

## Portfolio Value

Makes retry and resume behavior auditable by binding every attempt to one immutable deployment plan, preventing a superficially resumed deployment from switching artifacts or moving backward through safety checkpoints.

## Validation

Run python3 -m unittest discover -s tests and confirm stable ordered retries pass while changed deployment identity, mutable digests, duplicate attempts, regressed checkpoints, invalid timestamps, excessive retries, and invalid policy fail.
