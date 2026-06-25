# Add immutable image tag policy

<!-- daily-pr-task: image-tag-policy -->

Zero-downtime deployment needs immutable images. A release should point to a versioned tag or digest so rollback and audit are predictable.

Policy checks:

- image value is present
- `latest` is not used
- digest or explicit version tag is present
- registry path is documented

## Portfolio Value

Strengthens the deployment story by preventing mutable image tags in production releases.

## Validation

Run the unit test and confirm latest or empty tags are rejected.
