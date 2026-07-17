# Add promotion verification window policy

<!-- daily-pr-task: promotion-verification-window -->

A new color should remain under observation for multiple consecutive health samples before the previous color is decommissioned. A configurable verification window reduces the risk of treating a single transient success as release readiness.

## Portfolio Value

Strengthens health-gated promotion by requiring sustained readiness before rollback capacity is removed.

## Validation

Run `python3 -m unittest discover -s tests` and confirm a recent failed sample resets the promotion window.
