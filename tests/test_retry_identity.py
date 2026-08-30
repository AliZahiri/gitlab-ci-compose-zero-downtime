import unittest

from compose_zero_downtime.retry_identity import deployment_retry_is_safe, deployment_retry_violations


DIGEST = "sha256:" + "a" * 64


class DeploymentRetryIdentityEvidenceTests(unittest.TestCase):
    def test_same_release_with_forward_checkpoint_progress_passes(self):
        attempts = [
            {"attempt_id": "try-1", "deployment_id": "deploy-42", "environment": "prod", "target_color": "green", "image_digest": DIGEST, "last_completed_checkpoint": "candidate_started", "started_at": "2026-08-30T06:00:00Z"},
            {"attempt_id": "try-2", "deployment_id": "deploy-42", "environment": "prod", "target_color": "green", "image_digest": DIGEST, "last_completed_checkpoint": "health_checked", "started_at": "2026-08-30T06:05:00Z"},
        ]
        self.assertTrue(deployment_retry_is_safe(attempts))

    def test_changed_release_and_regressed_checkpoint_fail(self):
        attempts = [
            {"attempt_id": "try-1", "deployment_id": "deploy-42", "environment": "prod", "target_color": "green", "image_digest": DIGEST, "last_completed_checkpoint": "health_checked", "started_at": "2026-08-30T06:00:00Z"},
            {"attempt_id": "try-1", "deployment_id": "deploy-42", "environment": "prod", "target_color": "blue", "image_digest": "latest", "last_completed_checkpoint": "planned", "started_at": "2026-08-30T05:00:00Z"},
        ]
        violations = deployment_retry_violations(attempts)
        self.assertIn("attempt_1:attempt_id_must_be_unique", violations)
        self.assertIn("attempt_1:release_identity_changed_during_retry", violations)
        self.assertIn("attempt_1:checkpoint_regressed", violations)
        self.assertIn("attempt_1:attempt_time_must_increase", violations)

    def test_single_attempt_and_invalid_policy_fail(self):
        self.assertEqual(("at_least_two_deployment_attempts_are_required",), deployment_retry_violations([]))
        with self.assertRaises(ValueError):
            deployment_retry_violations([], maximum_attempts=1)
