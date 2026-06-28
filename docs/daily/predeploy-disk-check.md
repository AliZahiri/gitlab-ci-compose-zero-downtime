# Add pre-deploy disk check

<!-- daily-pr-task: predeploy-disk-check -->

Pre-deploy checks should verify enough free disk is available before pulling a new image or starting a new color. This prevents partial deployments caused by host capacity issues.

Checks:

- free disk percentage
- minimum free bytes
- image pull target filesystem
- fail-fast behavior

## Portfolio Value

Shows the deploy flow verifies host capacity before starting a new color.

## Validation

Run the unit test and confirm low free disk space blocks deployment.
