import unittest

from compose_zero_downtime.health_grace import health_grace_is_safe, health_grace_warnings


class HealthGraceTests(unittest.TestCase):
    def test_reasonable_grace_window_passes(self):
        self.assertTrue(health_grace_is_safe(warmup_seconds=60, interval_seconds=5))

    def test_oversized_grace_window_is_reported(self):
        self.assertIn("warmup_exceeds_max_grace", health_grace_warnings(warmup_seconds=300, interval_seconds=10))


if __name__ == "__main__":
    unittest.main()
