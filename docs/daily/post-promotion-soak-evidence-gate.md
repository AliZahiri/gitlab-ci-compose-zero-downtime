# Add post-promotion soak evidence gate

<!-- daily-pr-task: post-promotion-soak-evidence-gate -->

The old color should remain available until the promoted color has completed a measurable soak window. This offline gate validates promotion and observation timestamps, minimum traffic coverage, error ratio, p95 latency, rollback signals, and old-color availability before cleanup is allowed.

## Portfolio Value

Adds measurable post-switch evidence before old-color cleanup, preserving a tested rollback path through the period where regressions are most likely to surface.

## Validation

Run python3 -m unittest discover -s tests and confirm incomplete windows, insufficient traffic, excessive errors or latency, rollback signals, unavailable old color, malformed timestamps, and invalid policy fail.
