import unittest

from compose_zero_downtime.rollback_window import rollback_window_is_safe, rollback_window_warnings


class RollbackWindowTests(unittest.TestCase):
    def test_window_keeps_old_color_available(self):
        self.assertTrue(rollback_window_is_safe(keep_old_seconds=300, smoke_check_seconds=60))

    def test_short_window_is_reported(self):
        self.assertIn("rollback_window_too_short", rollback_window_warnings(keep_old_seconds=90, smoke_check_seconds=30))


if __name__ == "__main__":
    unittest.main()
