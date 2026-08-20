# Add promotion approval evidence gate

<!-- daily-pr-task: promotion-approval-evidence-gate -->

A health-gated blue-green promotion also needs a reviewable approval record. This offline gate validates an immutable candidate digest, change ticket, approver, timezone-aware approval time, active change window, and rollback readiness. It does not deploy or contact a CI service.

## Portfolio Value

Complements health checks with auditable human approval and immutable release evidence before traffic is promoted.

## Validation

Run `python3 -m unittest discover -s tests` and confirm only immutable, ticketed, time-bounded approvals with rollback readiness pass.
