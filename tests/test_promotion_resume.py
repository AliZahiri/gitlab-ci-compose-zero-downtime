import unittest

from compose_zero_downtime.promotion_resume import promotion_can_resume, promotion_resume_violations


def checkpoint():
    return {"release_id": "orders-20260725.1", "current_color": "blue", "candidate_color": "green", "candidate_digest": "sha256:" + "a" * 64, "states": ["prepared", "candidate_started", "candidate_healthy"], "rollback_ready": True}


class PromotionResumeCheckpointTests(unittest.TestCase):
    def test_ordered_immutable_checkpoint_can_resume(self):
        self.assertTrue(promotion_can_resume(checkpoint()))

    def test_digest_journal_and_rollback_failures_are_combined(self):
        invalid = checkpoint()
        invalid.update({"candidate_digest": "latest", "states": ["prepared", "candidate_healthy"], "rollback_ready": False})

        violations = promotion_resume_violations(invalid)

        self.assertIn("candidate_digest_must_be_immutable", violations)
        self.assertIn("journal:deployment_transition_order_is_invalid", violations)
        self.assertIn("rollback_readiness_must_be_confirmed", violations)

    def test_missing_journal_and_equal_colors_fail(self):
        invalid = checkpoint()
        invalid.update({"candidate_color": "blue", "states": None})
        violations = promotion_resume_violations(invalid)
        self.assertIn("candidate_color_must_differ_from_current_color", violations)
        self.assertIn("transition_journal_is_required", violations)


if __name__ == "__main__":
    unittest.main()
