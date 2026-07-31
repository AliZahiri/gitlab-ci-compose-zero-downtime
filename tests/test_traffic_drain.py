import unittest

from compose_zero_downtime.traffic_drain import old_color_is_safe_to_stop, traffic_drain_violations


class TrafficDrainGateTests(unittest.TestCase):
    def test_ordered_non_increasing_observations_reaching_zero_pass(self):
        observations = [{"observed_at": "2026-07-31T10:00:00Z", "in_flight_requests": 3}, {"observed_at": "2026-07-31T10:00:10Z", "in_flight_requests": 1}, {"observed_at": "2026-07-31T10:00:20Z", "in_flight_requests": 0}]
        self.assertTrue(old_color_is_safe_to_stop(observations))

    def test_request_growth_gap_and_nonzero_final_count_fail(self):
        observations = [{"observed_at": "2026-07-31T10:00:00Z", "in_flight_requests": 2}, {"observed_at": "2026-07-31T10:01:00Z", "in_flight_requests": 4}]
        violations = traffic_drain_violations(observations)
        self.assertIn("observation_1:sampling_interval_exceeds_maximum", violations)
        self.assertIn("observation_1:in_flight_requests_must_not_increase", violations)
        self.assertIn("traffic_drain_threshold_not_reached", violations)

    def test_insufficient_observations_and_invalid_policy_fail(self):
        self.assertEqual(("traffic_drain_observations_are_insufficient",), traffic_drain_violations([]))
        with self.assertRaises(ValueError):
            traffic_drain_violations([], maximum_interval_seconds=0)


if __name__ == "__main__":
    unittest.main()
