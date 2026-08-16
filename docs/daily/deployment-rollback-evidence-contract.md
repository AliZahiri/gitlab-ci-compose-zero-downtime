# Add deployment rollback evidence contract

<!-- daily-pr-task: deployment-rollback-evidence-contract -->

A blue-green rollback should be an evidenced decision rather than a shell command. This offline contract validates the active color, immutable target artifact, a bounded rollback decision timestamp, and a recorded health reason. It does not claim downtime-free switching; it makes rollback prerequisites explicit.

## Portfolio Value

Makes blue-green recovery evidence testable and keeps immutable artifacts, health evidence, and rollback decisions connected.

## Validation

Run `python3 -m unittest discover -s tests` and confirm records without a valid color, immutable digest, timezone-aware decision, or health reason fail.
