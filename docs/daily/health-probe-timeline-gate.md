# Add health probe timeline gate

<!-- daily-pr-task: health-probe-timeline-gate -->

A sequence of successful health booleans is not sufficient promotion evidence when timestamps are stale, out of order, or separated by gaps that hide restarts. This deterministic gate requires timezone-aware observations, strictly increasing timestamps, bounded sampling gaps, a fresh final observation, and a configured number of consecutive healthy samples before traffic promotion.

## Portfolio Value

Turns health-gated promotion into timestamped evidence that rejects stale, gapped, reordered, or non-consecutive observations before an Nginx traffic switch.

## Validation

Run `python3 -m unittest discover -s tests` and confirm recent ordered health windows pass while stale, gapped, future, malformed, unordered, unhealthy, and invalid-policy timelines fail.
