# Add deployment lock policy

<!-- daily-pr-task: deploy-lock-policy -->

A deployment lock prevents two pipeline runs from switching colors at the same time. The lock should have an owner and TTL so abandoned deploys can be recovered safely.

Policy fields:

- lock name
- owner
- ttl seconds
- release behavior

## Portfolio Value

Shows concurrent production deploys are serialized for predictable traffic switching.

## Validation

Run the unit test and confirm lock TTL must be positive.
