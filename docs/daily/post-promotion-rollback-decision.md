# Add post-promotion rollback decision policy

<!-- daily-pr-task: post-promotion-rollback-decision -->

During the verification window, rollback should be driven by explicit observations rather than operator intuition. The policy requests rollback when health checks fail, the error-rate budget is exceeded, or the configured consecutive failure threshold is reached; invalid counters and rates are rejected before deployment.

## Portfolio Value

Adds deterministic recovery behavior to the verification window and ties rollback to measurable health and error-budget signals.

## Validation

Run `python3 -m unittest discover -s tests` and confirm healthy observations stay promoted while each failure signal and invalid bound is covered.
