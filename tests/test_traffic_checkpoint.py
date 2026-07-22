import unittest

from compose_zero_downtime.traffic_checkpoint import traffic_checkpoint_is_ready, traffic_checkpoint_violations


class TrafficCheckpointTests(unittest.TestCase):
    def test_complete_checkpoint_passes(self):
        checkpoint = {"current_color": "blue", "candidate_color": "green", "candidate_digest": "sha256:" + "a" * 64, "candidate_healthy": True, "proxy_config_valid": True, "previous_upstream": "app_blue"}
        self.assertTrue(traffic_checkpoint_is_ready(checkpoint))

    def test_same_color_and_mutable_image_fail(self):
        checkpoint = {"current_color": "blue", "candidate_color": "blue", "candidate_digest": "latest", "candidate_healthy": True, "proxy_config_valid": True, "previous_upstream": "app_blue"}
        violations = traffic_checkpoint_violations(checkpoint)
        self.assertIn("candidate_must_differ_from_current_color", violations)
        self.assertIn("candidate_digest_must_be_immutable", violations)

    def test_health_proxy_and_rollback_state_are_required(self):
        violations = traffic_checkpoint_violations({"current_color": "blue", "candidate_color": "green", "candidate_digest": "sha256:" + "b" * 64})
        self.assertIn("candidate_health_must_be_confirmed", violations)
        self.assertIn("proxy_configuration_must_be_validated", violations)
        self.assertIn("previous_upstream_is_required_for_rollback", violations)


if __name__ == "__main__":
    unittest.main()
