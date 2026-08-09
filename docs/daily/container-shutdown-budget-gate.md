# Add container shutdown budget gate

<!-- daily-pr-task: container-shutdown-budget-gate -->

Blue-green rollback safety depends on giving an old container enough time to drain accepted requests and finish application shutdown before Compose sends SIGKILL. This offline contract validates unique service observations, SIGTERM handling, non-negative drain and termination estimates, and a stop-grace period that covers both estimates plus a configurable safety margin.

## Portfolio Value

Turns graceful shutdown from an assumption into a measurable Compose contract that protects in-flight requests during promotion, rollback, and container replacement.

## Validation

Run `python3 -m unittest discover -s tests` and confirm sufficiently budgeted SIGTERM shutdowns pass while empty evidence, duplicate services, unsafe signals, invalid durations, insufficient grace periods, and invalid margins fail.
