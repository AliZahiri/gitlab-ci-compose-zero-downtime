# Add release health budget gate

<!-- daily-pr-task: release-health-budget-gate -->

Promotion should be blocked when a release exceeds its explicit health budget. This helper keeps the gate deterministic by checking successful probes, allowed failures, and total observation duration before traffic changes.

## Portfolio Value

Makes blue-green promotion gates measurable and easier to explain in a production release review.

## Validation

Run `python3 -m unittest discover -s tests` and confirm failed probes block promotion by default.
