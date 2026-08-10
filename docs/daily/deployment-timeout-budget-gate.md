# Add deployment timeout budget gate

<!-- daily-pr-task: deployment-timeout-budget-gate -->

A blue/green promotion needs an explicit end-to-end timeout budget so a blocked pull, startup, health wait, or traffic switch cannot hold a deployment lock indefinitely. This offline gate validates declared stage budgets and observed durations. It requires positive budgets for pull, startup, health, and promotion; each observation must fit its stage and the total must fit the release budget. It does not run Docker, Nginx, or a deployment.

## Portfolio Value

Demonstrates bounded, observable release control across every promotion stage rather than treating individual health checks as an unlimited wait.

## Validation

Run `python3 -m unittest discover -s tests` and confirm compliant stage and total budgets pass while exceeded, negative, missing, and under-provisioned budgets fail.
