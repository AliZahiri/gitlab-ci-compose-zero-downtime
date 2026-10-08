# Add Compose service resource contract gate

<!-- daily-pr-task: compose-service-resource-contract-gate -->

Blue-green promotion needs enough capacity for both colours and predictable restart behavior. This offline contract validates declared per-service CPU, memory, restart policy, and readiness timeout before an orchestration plan is accepted. It validates configuration metadata only and does not start containers or inspect production infrastructure.

## Portfolio Value

Prevents a nominally healthy blue-green plan from promoting a colour with undeclared resource bounds or an unsafe readiness contract.

## Validation

Run python3 -m unittest discover -s tests and confirm services require unique names, positive CPU, policy-compliant memory, approved restart behavior, and bounded readiness timeouts.
