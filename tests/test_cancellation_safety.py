import unittest

from compose_zero_downtime.cancellation_safety import deployment_cancellation_is_safe, deployment_cancellation_violations


class DeploymentCancellationSafetyEvidenceTests(unittest.TestCase):
    def test_unswitched_candidate_cleanup_passes(self):
        evidence = {"deployment_id": "deploy-42", "cancelled_at": "2026-08-30T07:00:00Z", "traffic_switched": False, "safe_outcome": "candidate_stopped", "active_color_health_verified": True, "transition_journal_persisted": True, "deployment_lock_released": True}
        self.assertTrue(deployment_cancellation_is_safe(evidence))

    def test_switched_traffic_with_completed_rollback_passes(self):
        evidence = {"deployment_id": "deploy-43", "cancelled_at": "2026-08-30T07:05:00+00:00", "traffic_switched": True, "safe_outcome": "rollback_completed", "active_color_health_verified": True, "transition_journal_persisted": True, "deployment_lock_released": True}
        self.assertTrue(deployment_cancellation_is_safe(evidence))

    def test_ambiguous_switched_cancellation_fails_closed(self):
        evidence = {"deployment_id": "deploy-44", "cancelled_at": "2026-08-30T07:10:00", "traffic_switched": True, "safe_outcome": "candidate_stopped", "active_color_health_verified": False, "transition_journal_persisted": False, "deployment_lock_released": False}
        violations = deployment_cancellation_violations(evidence)
        self.assertIn("cancelled_at_must_be_timezone_aware", violations)
        self.assertIn("switched_traffic_requires_rollback_or_promotion_completion", violations)
        self.assertIn("active_color_health_must_be_verified", violations)
        self.assertIn("deployment_lock_must_be_released_after_safe_outcome", violations)
