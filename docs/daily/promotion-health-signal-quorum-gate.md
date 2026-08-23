# Add promotion health signal quorum gate

<!-- daily-pr-task: promotion-health-signal-quorum-gate -->

A blue-green promotion should not rely on one successful probe. This offline gate requires a configurable quorum of unique passing health signals, consecutive-success evidence, and timezone-aware observations before traffic promotion.

## Portfolio Value

Strengthens health-gated promotion by requiring independent stable evidence instead of allowing a single transient success to switch traffic.

## Validation

Run python3 -m unittest discover -s tests and confirm duplicate, failing, unstable, or naive-timestamped signals cannot satisfy promotion quorum.
