import unittest

from compose_zero_downtime.promotion_state_handoff import promotion_state_handoff_is_safe, promotion_state_handoff_violations


class PromotionStateHandoffGateTests(unittest.TestCase):
    def test_recoverable_handoff_passes(self):
        record = {"active_color": "blue", "standby_color": "green", "candidate_image_digest": "sha256:" + "a" * 64, "rollback_image_digest": "sha256:" + "b" * 64, "candidate_healthy": True, "rollback_ready": True}
        self.assertTrue(promotion_state_handoff_is_safe(record))

    def test_unrecoverable_handoff_fails(self):
        violations = promotion_state_handoff_violations({"active_color": "blue", "standby_color": "blue", "candidate_image_digest": "latest", "rollback_image_digest": "bad", "candidate_healthy": False, "rollback_ready": False})
        self.assertIn("active_and_standby_colors_must_be_distinct", violations)
        self.assertIn("candidate_image_digest_must_be_immutable", violations)
        self.assertIn("rollback_image_digest_must_be_immutable", violations)
        self.assertIn("candidate_health_must_pass", violations)
        self.assertIn("rollback_must_be_ready", violations)


if __name__ == "__main__":
    unittest.main()
