# Add traffic shift plan policy

<!-- daily-pr-task: traffic-shift-plan-policy -->

Traffic shift plan policy should keep blue/green promotion steps explicit. Traffic percentages must start at 0, finish at 100, and never move backwards.

Policy checks:

- starts at 0 percent
- ends at 100 percent
- percentages are ordered
- observation seconds are positive

## Portfolio Value

Shows compose promotion has controlled traffic movement and rollback points.

## Validation

Run the unit test and confirm traffic shift steps are ordered and bounded.
