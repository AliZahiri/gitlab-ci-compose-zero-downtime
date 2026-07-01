# Add compose health grace policy

<!-- daily-pr-task: compose-health-grace-policy -->

Compose health grace policy should define how long a new color is allowed to warm up before traffic promotion. The window must be long enough for startup but bounded for CI feedback.

Policy fields:

- warmup seconds
- health interval seconds
- maximum grace seconds
- failure action

## Portfolio Value

Shows blue/green promotion waits for readiness without hiding broken deployments.

## Validation

Run the unit test and confirm grace windows are bounded and positive.
