import unittest

from compose_zero_downtime.resource_headroom import dual_color_headroom_violations, host_has_dual_color_headroom


class DualColorResourceHeadroomGateTests(unittest.TestCase):
    def test_memory_and_disk_with_reserved_margin_pass(self):
        resources = {"memory_mb": {"available": 2000, "candidate_required": 1200}, "disk_mb": {"available": 5000, "candidate_required": 3000}}
        self.assertTrue(host_has_dual_color_headroom(resources))

    def test_missing_memory_and_insufficient_disk_fail(self):
        violations = dual_color_headroom_violations({"disk_mb": {"available": 1000, "candidate_required": 900}})
        self.assertIn("resource:memory_mb:observation_is_required", violations)
        self.assertIn("resource:disk_mb:dual_color_headroom_is_insufficient", violations)

    def test_invalid_measurement_and_margin_fail(self):
        violations = dual_color_headroom_violations({"memory_mb": {"available": True, "candidate_required": 10}, "disk_mb": {"available": 10, "candidate_required": 0}})
        self.assertEqual(2, len(violations))
        with self.assertRaises(ValueError):
            dual_color_headroom_violations({}, safety_margin_ratio=1)


if __name__ == "__main__":
    unittest.main()
