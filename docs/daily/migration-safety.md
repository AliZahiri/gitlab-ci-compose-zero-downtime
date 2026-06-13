# Add migration safety notes

<!-- daily-pr-task: migration-safety -->

Zero-downtime deployment depends on backward-compatible database changes. A container switch cannot protect against destructive schema changes.

Safer migration pattern:

- expand schema first
- deploy app code that supports old and new schema
- backfill data if needed
- switch traffic after readiness checks
- remove old schema only after all app instances are upgraded

## Portfolio Value

Shows awareness of the boundary between deployment mechanics and application compatibility.

## Validation

Review the markdown file and confirm it warns about breaking migrations.
