# Add compose profile policy

<!-- daily-pr-task: compose-profile-policy -->

Compose profile policy should verify that both blue and green profiles exist and that shared infrastructure is not accidentally color-scoped. This keeps the deployment topology predictable.

Required profiles:

- blue
- green
- shared proxy service outside app color lifecycle

## Portfolio Value

Keeps the blue/green Compose layout explicit and reviewable.

## Validation

Run the unit test and confirm both color profiles are required.
