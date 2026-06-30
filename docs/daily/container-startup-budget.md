# Add container startup budget policy

<!-- daily-pr-task: container-startup-budget -->

Container startup budget should define how long the deployer waits before failing a color promotion. Bounded waits prevent stuck pipelines.

Policy fields:

- health attempts
- health interval seconds
- maximum startup budget
- failure action

## Portfolio Value

Shows readiness waits are bounded and tuned to deployment expectations.

## Validation

Run the unit test and confirm startup attempts and intervals are bounded.
