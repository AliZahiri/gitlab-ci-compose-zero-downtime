# Add Nginx worker drain evidence gate

<!-- daily-pr-task: nginx-worker-drain-evidence-gate -->

Reloading Nginx does not prove that old workers drained before the previous application color was removed. This offline gate validates a bounded, monotonic active-connection timeline, requires the old worker generation to reach zero, confirms the candidate upstream remains healthy, and preserves rollback readiness through the drain window.

## Portfolio Value

Makes proxy reload and old-color teardown depend on observed connection drain while health and rollback safeguards remain intact.

## Validation

Run python3 -m unittest discover -s tests and confirm monotonic healthy drain to zero passes while connection regressions, unhealthy candidates, lost rollback readiness, timeouts, malformed samples, and invalid policy fail.
