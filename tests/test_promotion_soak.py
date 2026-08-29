import unittest

from compose_zero_downtime.promotion_soak import promotion_soak_is_complete, promotion_soak_violations


class PostPromotionSoakEvidenceTests(unittest.TestCase):
    def test_observed_healthy_soak_with_rollback_path_passes(self):
        evidence = {"promoted_at": "2026-08-29T08:00:00Z", "observed_at": "2026-08-29T08:30:00Z", "request_count": 1000, "error_count": 2, "p95_latency_ms": 420, "rollback_triggered": False, "old_color_available": True}
        self.assertTrue(promotion_soak_is_complete(evidence))

    def test_short_under_sampled_unhealthy_soak_fails(self):
        evidence = {"promoted_at": "2026-08-29T08:00:00Z", "observed_at": "2026-08-29T08:01:00Z", "request_count": 20, "error_count": 5, "p95_latency_ms": 2500, "rollback_triggered": True, "old_color_available": False}
        violations = promotion_soak_violations(evidence)
        self.assertIn("promotion_soak_window_is_incomplete", violations)
        self.assertIn("request_count_is_below_soak_minimum", violations)
        self.assertIn("promotion_error_rate_exceeds_budget", violations)
        self.assertIn("old_color_must_remain_available_during_soak", violations)

    def test_invalid_policy_is_rejected(self):
        with self.assertRaises(ValueError):
            promotion_soak_violations({}, minimum_soak_seconds=0)
