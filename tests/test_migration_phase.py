import unittest

from compose_zero_downtime.migration_phase import migration_phase_is_safe_for_promotion, migration_phase_violations


class MigrationExpandContractPhaseTests(unittest.TestCase):
    def test_successful_compatible_expand_with_pending_contract_passes(self):
        evidence = {"release_id": "2026.08.29", "schema_version": "42", "migration_checksum": "sha256:abc", "backward_compatible": True, "old_color_rollback_eligible": True, "phases": [{"name": "expand", "status": "succeeded"}, {"name": "backfill", "status": "running"}, {"name": "contract", "status": "pending"}]}
        self.assertTrue(migration_phase_is_safe_for_promotion(evidence))

    def test_failed_expand_and_early_contract_fail(self):
        evidence = {"release_id": "r2", "schema_version": "43", "migration_checksum": "sha256:def", "backward_compatible": False, "old_color_rollback_eligible": True, "phases": [{"name": "expand", "status": "pending"}, {"name": "contract", "status": "succeeded"}]}
        violations = migration_phase_violations(evidence)
        self.assertIn("expand_phase_must_succeed_before_promotion", violations)
        self.assertIn("expanded_schema_must_be_backward_compatible", violations)
        self.assertIn("contract_phase_must_wait_until_rollback_window_closes", violations)

    def test_duplicate_and_unknown_phases_fail(self):
        violations = migration_phase_violations({"release_id": "r3", "schema_version": "44", "migration_checksum": "sha256:ghi", "backward_compatible": True, "old_color_rollback_eligible": False, "phases": [{"name": "expand", "status": "succeeded"}, {"name": "expand", "status": "succeeded"}, {"name": "drop", "status": "done"}]})
        self.assertIn("phase_1:name_must_be_unique", violations)
        self.assertIn("phase_2:name_is_invalid", violations)
