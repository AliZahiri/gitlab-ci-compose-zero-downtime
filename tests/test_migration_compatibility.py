import unittest

from compose_zero_downtime.migration_compatibility import migration_compatibility_violations, migration_is_safe_to_promote


class MigrationCompatibilityEvidenceGateTests(unittest.TestCase):
    def test_compatible_migration_with_rollback_evidence_passes(self):
        self.assertTrue(migration_is_safe_to_promote({"migration_id": "20260820_add_index", "strategy": "expand-contract", "backward_compatibility_checked": True, "rollback_tested": True}))

    def test_missing_or_unverified_controls_are_reported(self):
        violations = migration_compatibility_violations({"migration_id": "", "strategy": "breaking", "backward_compatibility_checked": False, "rollback_tested": False})
        self.assertEqual(violations, ("migration_id_is_required", "strategy_must_be_compatible", "backward_compatibility_check_must_pass", "rollback_test_must_pass"))
