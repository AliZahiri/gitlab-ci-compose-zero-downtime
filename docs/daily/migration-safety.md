# Migration Safety For Zero-Downtime Deployments

Zero-downtime deployment depends on backward-compatible database changes. A
container switch cannot protect against destructive schema changes.

Safer migration pattern:

- expand schema first
- deploy app code that supports old and new schema
- backfill data if needed
- switch traffic after readiness checks
- remove old schema only after all app instances are upgraded

The deployment pipeline should treat schema compatibility as part of release
readiness. Blue-green Docker Compose deployment can keep processes available,
but application and database versions still need a contract that both colors can
serve during the transition.
