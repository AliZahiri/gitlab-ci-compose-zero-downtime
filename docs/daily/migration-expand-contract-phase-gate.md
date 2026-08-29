# Add migration expand-contract phase gate

<!-- daily-pr-task: migration-expand-contract-phase-gate -->

A blue-green release must separate additive schema expansion from destructive contraction. This offline gate validates supplied migration phase evidence, requires a successful backward-compatible expand phase before promotion, and blocks a completed contract phase while the old color remains rollback-eligible. It does not connect to a production database.

## Portfolio Value

Makes database migration sequencing explicit so blue-green rollback remains credible while additive and destructive schema changes progress independently.

## Validation

Run python3 -m unittest discover -s tests and confirm missing or duplicate phases, incomplete expansion, incompatible schemas, invalid statuses, and early contraction fail.
