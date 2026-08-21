# Add deployment recovery budget contract

<!-- daily-pr-task: deployment-recovery-budget-contract -->

Recovery claims are meaningful only when they are bounded and verified. This contract validates a positive recovery budget, an observed recovery duration within that budget, confirmation that rollback restored the previous target, and a timezone-aware observation time.

## Portfolio Value

Turns rollback readiness into a measurable recovery objective with evidence that the previous target became healthy again.

## Validation

Run `python3 -m unittest discover -s tests` and confirm recovery must be completed, health-verified, timestamped, and within its declared budget.
