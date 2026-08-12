# Add migration rollback contract gate

<!-- daily-pr-task: migration-rollback-contract -->

A promotion can only claim rollback readiness when its data migration has explicit compatibility and recovery intent. This offline gate validates migration metadata: a unique migration identifier, forward-compatible state, an explicit rollback strategy, and a verified backup reference. It checks planning evidence only and does not connect to a database.

## Portfolio Value

Connects blue/green traffic safety to the often riskier database layer with concrete evidence for compatibility and recovery.

## Validation

Run `python3 -m unittest discover -s tests` and confirm compatible migrations with verified recovery pass while empty, duplicate, incompatible, rollback-undefined, and backup-unverified evidence fails.
