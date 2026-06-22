# Add deployment environment variable notes

<!-- daily-pr-task: deploy-env-vars -->

Deployment variables should be explicit so teams can reuse the template safely.

Important variables:

- `DEPLOY_HOST` and `DEPLOY_USER` for SSH target selection
- `DEPLOY_PATH` for server-side release location
- `APP_IMAGE` for the immutable image promoted to a color
- `STOP_OLD_AFTER_SWITCH` for keeping or stopping the old color
- `APP_PORT` for internal app readiness checks

## Portfolio Value

Improves template usability for real GitLab CI deployment scenarios.

## Validation

Review the markdown file and confirm variable names match repository conventions.
