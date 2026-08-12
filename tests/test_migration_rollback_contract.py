import unittest

from compose_zero_downtime.migration_rollback_contract import migration_rollback_contract_is_safe, migration_rollback_contract_violations


class MigrationRollbackContractGateTests(unittest.TestCase):
    def test_compatible_verified_migration_passes(self):
        migrations = [{"migration_id": "20260811-add-index", "forward_compatible": True, "rollback_strategy": "no_schema_change", "backup_verified": True}]
        self.assertTrue(migration_rollback_contract_is_safe(migrations))

    def test_duplicate_incompatible_and_unverified_migrations_fail(self):
        migrations = [{"migration_id": "20260811-add-index", "forward_compatible": False, "rollback_strategy": "", "backup_verified": False}, {"migration_id": "20260811-add-index", "forward_compatible": True, "rollback_strategy": "restore_backup", "backup_verified": True}]
        violations = migration_rollback_contract_violations(migrations)
        self.assertIn("migration_0:must_be_forward_compatible", violations)
        self.assertIn("migration_0:rollback_strategy_must_be_explicit", violations)
        self.assertIn("migration_0:backup_must_be_verified", violations)
        self.assertIn("migration_1:migration_id_must_be_unique", violations)


if __name__ == "__main__":
    unittest.main()
