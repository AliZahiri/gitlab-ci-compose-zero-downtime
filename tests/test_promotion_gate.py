import unittest

from compose_zero_downtime.promotion_gate import promotion_gate_violations, promotion_is_ready


def checkpoint():
    return {"current_color": "blue", "candidate_color": "green", "candidate_digest": "sha256:" + "a" * 64, "candidate_healthy": True, "proxy_config_valid": True, "previous_upstream": "app_blue"}


class PromotionGateTests(unittest.TestCase):
    def test_recoverable_healthy_release_is_ready(self):
        self.assertTrue(promotion_is_ready(checkpoint=checkpoint(), health_samples=[True, True, True], health_summary={"successes": 3, "failures": 0}))

    def test_checkpoint_window_and_budget_failures_are_combined(self):
        invalid = checkpoint()
        invalid["proxy_config_valid"] = False
        violations = promotion_gate_violations(checkpoint=invalid, health_samples=[True, False], health_summary={"successes": 1, "failures": 1})
        self.assertIn("proxy_configuration_must_be_validated", violations)
        self.assertIn("promotion_health_window_not_satisfied", violations)
        self.assertIn("failed_probes_exceed_budget", violations)


if __name__ == "__main__":
    unittest.main()
