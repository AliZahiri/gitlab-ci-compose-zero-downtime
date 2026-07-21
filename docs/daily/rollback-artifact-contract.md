# Add rollback artifact availability contract

<!-- daily-pr-task: rollback-artifact-contract -->

Rollback readiness depends on more than a healthy previous container. The previous image must be pinned by immutable digest, remain available to the deployment runner, differ from the candidate digest, and retain trusted verification evidence. This contract checks those prerequisites before promotion removes rollback capacity.

## Portfolio Value

Adds an immutable artifact and provenance gate to rollback planning instead of assuming the previous image remains pullable and trusted.

## Validation

Run `python3 -m unittest discover -s tests` and confirm mutable, unavailable, unverified, or candidate-equal rollback artifacts fail validation.
