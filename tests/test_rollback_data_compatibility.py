import unittest

from compose_zero_downtime.rollback_data_compatibility import rollback_data_compatibility_violations, rollback_data_is_compatible


class RollbackDataCompatibilityTests(unittest.TestCase):
    def test_supported_schema_with_verified_recovery_evidence_passes(self):
        evidence = {"rollback_image_digest": "sha256:" + "a" * 64, "current_schema_version": 12, "rollback_min_schema_version": 10, "rollback_max_schema_version": 12, "migration_reversible": True, "rollback_forward_compatible": False, "backup_verified": True}
        self.assertTrue(rollback_data_is_compatible(evidence))

    def test_unsupported_schema_and_missing_recovery_evidence_fail(self):
        violations = rollback_data_compatibility_violations({"rollback_image_digest": "latest", "current_schema_version": 13, "rollback_min_schema_version": 10, "rollback_max_schema_version": 12, "migration_reversible": False, "rollback_forward_compatible": False, "backup_verified": False})
        self.assertIn("current_schema_is_not_supported_by_rollback_target", violations)
        self.assertIn("migration_requires_reversibility_or_forward_compatibility", violations)
        self.assertIn("verified_backup_is_required_before_rollback", violations)
