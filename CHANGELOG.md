# Changelog

All notable changes to this project are documented in this file.

The project follows Semantic Versioning for public release snapshots. Policy
helpers and evidence schemas remain experimental unless their documentation
states otherwise.

## [0.2.0] - Unreleased

### Added

- Promotion-resume validation in the Python deployment CLI, with structured
  checkpoint decisions for pipeline integration.
- Release controls for immutable image identity, artifact provenance and age,
  platform compatibility, SBOM and signature evidence, configuration
  fingerprints, and rendered Compose provenance.
- Promotion evidence contracts covering readiness, health budgets and quorum,
  observation ordering, soak windows, approval, checkpoints, transition
  journals, runtime identity, restart stability, and rollback decisions.
- Safety policies for concurrent deployments, lock leases, retry identity,
  cancellation, resource headroom, service dependencies, network and volume
  isolation, listener ownership, traffic drain, and Nginx worker drain.
- Migration controls for expand-contract sequencing, backup evidence,
  compatibility, execution evidence, data compatibility, and rollback plans.
- Operational controls for credential redaction, log correlation, dependency
  health, database connection budgets, recovery budgets, and rollback
  execution evidence.

### Changed

- Daily portfolio automation validates backlog inputs and generated paths,
  isolates validation in a temporary worktree, and requires successful PR
  checks before auto-merge.
- GitHub Actions dependencies were upgraded to their Node 24-compatible major
  versions.

### Fixed

- Container readiness rejects stopped candidates and the CLI starts reliably
  through both module and installed-script entry points.
- Rollback execution evidence now fails closed on malformed, stale, future,
  mismatched, or unsuccessful observations.
- Automated commits preserve the configured Git attribution.

### Security

- Deployment evidence is bound to the approved environment, release identity,
  and immutable image digest.
- Generated output destinations reject traversal and repository-control paths.
- Secret references and credential-redaction evidence are validated without
  storing production credentials in the repository.

### Compatibility

- The package and CLI require Python 3.10 or newer.
- Existing Bash and Python deployment commands remain available.
- No persisted-data migration is required, but adopters must review the new
  evidence gates before making them mandatory in an existing pipeline.

[0.2.0]: https://github.com/AliZahiri/gitlab-ci-compose-zero-downtime/compare/v0.1.0...v0.2.0
