import unittest

from compose_zero_downtime.migration_plan import migration_plan_is_safe, migration_plan_warnings


class MigrationPlanTests(unittest.TestCase):
    def test_expand_before_verified_contract_passes(self):
        steps = [{"phase": "expand"}, {"phase": "backfill"}, {"phase": "contract", "compatibility_window_complete": True, "rollback_tested": True}]
        self.assertTrue(migration_plan_is_safe(steps))

    def test_contract_requires_compatibility_and_rollback_evidence(self):
        warnings = migration_plan_warnings([{"phase": "expand"}, {"phase": "contract"}])
        self.assertIn("step_1_compatibility_window_incomplete", warnings)
        self.assertIn("step_1_rollback_not_tested", warnings)

    def test_contract_cannot_precede_expand(self):
        warnings = migration_plan_warnings([{"phase": "contract", "compatibility_window_complete": True, "rollback_tested": True}])
        self.assertIn("expand_must_precede_contract", warnings)


if __name__ == "__main__":
    unittest.main()
