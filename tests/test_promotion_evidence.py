import unittest

from compose_zero_downtime.promotion_evidence import promotion_evidence_is_complete, promotion_evidence_violations


def complete_evidence():
    return {"release_id": "orders-20260725.1", "current_color": "blue", "candidate_color": "green", "successful_health_samples": 5, "candidate_healthy": True, "proxy_config_validated": True, "smoke_tests_passed": True, "traffic_switch_succeeded": True, "rollback_ready": True}


class PromotionEvidenceTests(unittest.TestCase):
    def test_complete_promotion_evidence_passes(self):
        self.assertTrue(promotion_evidence_is_complete(complete_evidence(), minimum_health_samples=3))

    def test_color_health_proxy_and_rollback_failures_are_combined(self):
        evidence = complete_evidence()
        evidence.update({"candidate_color": "blue", "successful_health_samples": 1, "proxy_config_validated": False, "rollback_ready": False})

        violations = promotion_evidence_violations(evidence, minimum_health_samples=3)

        self.assertIn("candidate_color_must_differ_from_current_color", violations)
        self.assertIn("successful_health_samples_below_minimum", violations)
        self.assertIn("proxy_config_validated_must_be_confirmed", violations)
        self.assertIn("rollback_ready_must_be_confirmed", violations)

    def test_boolean_sample_count_and_invalid_policy_are_rejected(self):
        evidence = complete_evidence()
        evidence["successful_health_samples"] = True
        self.assertIn("successful_health_samples_below_minimum", promotion_evidence_violations(evidence))
        with self.assertRaises(ValueError):
            promotion_evidence_violations(evidence, minimum_health_samples=0)


if __name__ == "__main__":
    unittest.main()
