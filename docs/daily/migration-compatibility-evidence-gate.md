# Add migration compatibility evidence gate

<!-- daily-pr-task: migration-compatibility-evidence-gate -->

A blue-green release can still fail if its database migration is incompatible with the currently serving color. This offline gate requires an identified migration, a declared expand/contract compatibility strategy, a completed backwards-compatibility check, and an explicit rollback result before promotion. It validates release metadata only and does not run migrations.

## Portfolio Value

Prevents a database migration from undermining otherwise health-gated blue-green promotion.

## Validation

Run `python3 -m unittest discover -s tests` and verify only a compatible, rollback-tested migration can pass.
