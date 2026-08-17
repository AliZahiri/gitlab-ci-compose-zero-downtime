# Add release health evidence freshness gate

<!-- daily-pr-task: release-health-evidence-freshness-gate -->

A blue-green promotion should rely on recent, target-specific health evidence rather than a stale successful probe. This offline gate validates timezone-aware observations, a bounded evidence age, the candidate color, and a passing health result before a promotion can be considered.

## Portfolio Value

Connects promotion readiness to bounded, candidate-specific health evidence without claiming that a health check alone guarantees zero downtime.

## Validation

Run `python3 -m unittest discover -s tests` and confirm only recent, healthy blue or green candidate evidence passes.
