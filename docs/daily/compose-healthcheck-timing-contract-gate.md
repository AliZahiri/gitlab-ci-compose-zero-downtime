# Add Compose health-check timing contract gate

<!-- daily-pr-task: compose-healthcheck-timing-contract-gate -->

Promotion safety depends on a health check having enough time to observe startup and a bounded time to fail. This offline gate validates declarative health-check timing metadata: positive intervals and timeouts, a timeout no larger than its interval, sufficient retries, and a bounded worst-case readiness window. It does not execute commands or start containers.

## Portfolio Value

Makes readiness timing explicit and bounded before traffic promotion, strengthening the relationship between health checks and rollback expectations.

## Validation

Run python3 -m unittest discover -s tests and confirm bounded timing passes while zero values, oversized timeouts, and excessive readiness windows fail.
