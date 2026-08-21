import unittest

from compose_zero_downtime.recovery_budget import recovery_budget_violations, recovery_is_within_budget


class DeploymentRecoveryBudgetContractTests(unittest.TestCase):
    def test_verified_recovery_within_budget_passes(self):
        report = {"max_recovery_seconds": 120, "observed_recovery_seconds": 45, "previous_target_healthy": True, "rollback_completed": True, "observed_at": "2026-08-20T12:00:00Z"}
        self.assertTrue(recovery_is_within_budget(report))

    def test_overdue_or_unverified_recovery_fails(self):
        violations = recovery_budget_violations({"max_recovery_seconds": 60, "observed_recovery_seconds": 61, "previous_target_healthy": False, "rollback_completed": False, "observed_at": "2026-08-20T12:00:00"})
        self.assertEqual(violations, ("recovery_duration_exceeds_budget", "previous_target_health_must_be_confirmed", "rollback_must_complete", "observed_at_must_be_timezone_aware"))
