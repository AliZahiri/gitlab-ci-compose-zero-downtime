import unittest

from compose_zero_downtime.migration_execution_evidence import (
    migration_execution_evidence_is_safe,
    migration_execution_evidence_violations,
)


class MigrationExecutionEvidenceGateTests(unittest.TestCase):
    def test_bounded_compatible_migration_evidence_passes(self):
        evidence = {
            "migration_id": "expand-orders-v4",
            "release_id": "orders-2026.08.21",
            "duration_seconds": 42,
            "backward_compatible": True,
            "lock_wait_exceeded": False,
            "completed_at": "2026-08-21T12:00:00Z",
        }

        self.assertTrue(migration_execution_evidence_is_safe(evidence))

    def test_overdue_or_unsafe_execution_evidence_fails(self):
        violations = migration_execution_evidence_violations(
            {
                "migration_id": "",
                "release_id": "",
                "duration_seconds": 301,
                "backward_compatible": False,
                "lock_wait_exceeded": True,
                "completed_at": "2026-08-21T12:00:00",
            },
            maximum_duration_seconds=300,
        )

        self.assertEqual(
            violations,
            (
                "migration_id_is_required",
                "release_id_is_required",
                "migration_duration_exceeds_budget",
                "migration_must_be_backward_compatible",
                "migration_lock_wait_must_not_exceed_budget",
                "completed_at_must_be_timezone_aware",
            ),
        )

    def test_invalid_duration_policy_is_rejected(self):
        with self.assertRaises(ValueError):
            migration_execution_evidence_violations({}, maximum_duration_seconds=0)


if __name__ == "__main__":
    unittest.main()
