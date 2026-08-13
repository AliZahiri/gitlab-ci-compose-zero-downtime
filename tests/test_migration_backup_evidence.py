import unittest
from datetime import datetime, timezone

from compose_zero_downtime.migration_backup_evidence import migration_backup_evidence_is_ready, migration_backup_evidence_violations


NOW = datetime(2026, 8, 13, 6, 0, tzinfo=timezone.utc)


def evidence() -> dict[str, object]:
    return {"migration_id": "20260813_add_index", "backup_id": "postgres-20260813T055500Z", "backup_sha256": "a" * 64, "backup_encrypted": True, "restore_verified": True, "backup_completed_at": "2026-08-13T05:55:00Z", "restore_verified_at": "2026-08-13T05:58:00Z"}


class MigrationBackupRecoveryEvidenceGateTests(unittest.TestCase):
    def test_fresh_encrypted_backup_and_restore_evidence_passes(self):
        self.assertTrue(migration_backup_evidence_is_ready(evidence(), now=NOW))

    def test_invalid_unencrypted_unverified_and_stale_evidence_fails(self):
        candidate = evidence()
        candidate.update({"migration_id": "../unsafe", "backup_sha256": "bad", "backup_encrypted": False, "restore_verified": False, "backup_completed_at": "2026-08-13T03:00:00Z", "restore_verified_at": "2026-08-13T03:00:00Z"})
        violations = migration_backup_evidence_violations(candidate, now=NOW)
        self.assertIn("migration_id_is_invalid", violations)
        self.assertIn("backup_sha256_is_invalid", violations)
        self.assertIn("backup_must_be_encrypted", violations)
        self.assertIn("restore_must_be_verified", violations)
        self.assertIn("backup_completed_at_is_stale", violations)
        self.assertIn("restore_verified_at_is_stale", violations)

    def test_invalid_policy_and_naive_clock_fail(self):
        with self.assertRaises(ValueError):
            migration_backup_evidence_violations({}, now=NOW, maximum_age_seconds=0)
        with self.assertRaises(ValueError):
            migration_backup_evidence_violations({}, now=datetime(2026, 8, 13, 6, 0))


if __name__ == "__main__":
    unittest.main()
