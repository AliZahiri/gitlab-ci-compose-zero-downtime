import unittest

from compose_zero_downtime.rollback_window import rollback_window_is_safe, rollback_window_warnings


class RollbackWindowTests(unittest.TestCase):
    def test_safe_window_passes(self):
        self.assertTrue(rollback_window_is_safe(smoke_seconds=60, observation_seconds=300))

    def test_short_window_is_reported(self):
        warnings = rollback_window_warnings(smoke_seconds=10, observation_seconds=20)

        self.assertIn("rollback_window_too_short", warnings)


if __name__ == "__main__":
    unittest.main()
