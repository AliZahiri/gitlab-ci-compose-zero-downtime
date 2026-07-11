import unittest

from compose_zero_downtime.freeze_window import deployment_allowed, freeze_window_reason


class FreezeWindowTests(unittest.TestCase):
    def test_deployment_is_blocked_during_frozen_hour(self):
        self.assertFalse(deployment_allowed(22, {22, 23}))
        self.assertIn("22:00 UTC", freeze_window_reason(22, {22}))

    def test_emergency_override_allows_deployment(self):
        self.assertTrue(deployment_allowed(22, {22}, emergency_override=True))

    def test_invalid_hour_is_rejected(self):
        with self.assertRaises(ValueError):
            deployment_allowed(24, set())


if __name__ == "__main__":
    unittest.main()
