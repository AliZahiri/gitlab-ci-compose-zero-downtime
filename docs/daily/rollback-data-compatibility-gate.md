# Add rollback data compatibility gate

<!-- daily-pr-task: rollback-data-compatibility-gate -->

A healthy previous container is not a safe rollback target when a migration has made persisted data incompatible. This offline gate binds the rollback image digest to a supported database schema range and requires either reversible migrations or explicit forward compatibility plus verified backup evidence.

## Portfolio Value

Prevents a misleading container-only rollback decision by checking persisted-data compatibility and recovery evidence before traffic reversal.

## Validation

Run python3 -m unittest discover -s tests and confirm invalid digests, unsupported schemas, irreversible incompatible migrations, and unverified backups fail.
