# Add post-switch smoke test plan

<!-- daily-pr-task: smoke-test-plan -->

After switching traffic, a smoke test should verify the public path through the proxy, not only the container health state.

Minimum smoke tests:

- public HTTP endpoint returns success
- response identifies the expected app version or color when available
- critical API route responds within the expected timeout
- error rate remains stable after the switch

## Portfolio Value

Shows practical release validation beyond container orchestration.

## Validation

Review the markdown file and confirm smoke tests are externally observable.
