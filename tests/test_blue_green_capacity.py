import unittest

from compose_zero_downtime.blue_green_capacity import blue_green_capacity_is_ready, blue_green_capacity_violations


class BlueGreenCapacityPreflightTests(unittest.TestCase):
    def test_distinct_healthy_colors_with_headroom_pass(self):
        evidence = {"active_color": "blue", "candidate_color": "green", "active_healthy_replicas": 2, "candidate_healthy_replicas": 2, "expected_peak_connections": 100, "candidate_available_connections": 130, "rollback_capacity_reserved": True, "candidate_health_quorum_met": True}
        self.assertTrue(blue_green_capacity_is_ready(evidence))

    def test_same_color_insufficient_capacity_and_lost_rollback_fail(self):
        evidence = {"active_color": "blue", "candidate_color": "blue", "active_healthy_replicas": 1, "candidate_healthy_replicas": 0, "expected_peak_connections": 100, "candidate_available_connections": 100, "rollback_capacity_reserved": False, "candidate_health_quorum_met": False}
        violations = blue_green_capacity_violations(evidence)
        self.assertIn("candidate_color_must_differ_from_active_color", violations)
        self.assertIn("active_healthy_replicas_is_below_minimum", violations)
        self.assertIn("candidate_connection_headroom_is_insufficient", violations)
        self.assertIn("rollback_capacity_must_be_reserved", violations)

    def test_invalid_policy_fails(self):
        with self.assertRaises(ValueError):
            blue_green_capacity_violations({}, minimum_healthy_replicas=0)
