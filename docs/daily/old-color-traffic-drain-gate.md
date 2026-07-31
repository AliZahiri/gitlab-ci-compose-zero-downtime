# Add old-color traffic drain gate

<!-- daily-pr-task: old-color-traffic-drain-gate -->

Stopping the old color immediately after a proxy switch can terminate requests that were accepted before promotion. This deterministic gate validates a bounded sequence of timezone-aware in-flight request observations, requires strictly increasing timestamps and non-increasing request counts, rejects sampling gaps, and permits shutdown only after the final count reaches the configured drain threshold.

## Portfolio Value

Adds the missing shutdown-side safety evidence to blue-green promotion so the old color is retained until pre-switch requests have measurably drained.

## Validation

Run `python3 -m unittest discover -s tests` and confirm ordered draining traffic passes while insufficient samples, invalid counts, non-monotonic timestamps, excessive gaps, request growth, nonzero final counts, and invalid policy values fail.
