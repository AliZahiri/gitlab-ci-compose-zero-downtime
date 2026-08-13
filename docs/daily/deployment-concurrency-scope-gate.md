# Add deployment concurrency scope gate

<!-- daily-pr-task: deployment-concurrency-scope-gate -->

Concurrent blue/green promotions must not manipulate the same environment or traffic target at once. This offline gate validates active deployment leases: unique lease IDs, unique environment and traffic target ownership, timezone-aware expiry, and a positive bounded lease duration. It evaluates metadata only and does not acquire a lock.

## Portfolio Value

Makes deployment serialization visible at the environment and traffic-target level, not merely as a generic CI lock.

## Validation

Run `python3 -m unittest discover -s tests` and confirm unique bounded leases pass while empty input, duplicate ownership, malformed or expired timestamps, and invalid policy values fail.
