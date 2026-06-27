# Add Nginx config validation plan

<!-- daily-pr-task: nginx-config-validation-plan -->

Nginx configuration should be rendered and validated before reload. A failed validation must stop promotion and keep the previous color serving traffic.

Validation inputs:

- rendered config path
- validation command
- reload command
- rollback behavior

## Portfolio Value

Makes proxy reload safety explicit before traffic is switched.

## Validation

Run the unit test and confirm reload is blocked when validation fails.
