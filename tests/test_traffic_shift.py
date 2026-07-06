import unittest

from compose_zero_downtime.traffic_shift import traffic_shift_plan_is_safe, traffic_shift_warnings


class TrafficShiftTests(unittest.TestCase):
    def test_ordered_shift_plan_passes(self):
        steps = [{"percent": 0, "observe_seconds": 10}, {"percent": 50, "observe_seconds": 30}, {"percent": 100, "observe_seconds": 60}]

        self.assertTrue(traffic_shift_plan_is_safe(steps))

    def test_unordered_shift_plan_is_reported(self):
        warnings = traffic_shift_warnings([{"percent": 0, "observe_seconds": 10}, {"percent": 100, "observe_seconds": 10}, {"percent": 50, "observe_seconds": 10}])

        self.assertIn("traffic_shift_must_end_at_full", warnings)
        self.assertIn("traffic_shift_percentages_must_be_ordered", warnings)


if __name__ == "__main__":
    unittest.main()
