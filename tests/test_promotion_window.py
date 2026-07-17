import unittest

from compose_zero_downtime.promotion_window import consecutive_healthy_samples, promotion_window_is_satisfied


class PromotionWindowTests(unittest.TestCase):
    def test_required_consecutive_samples_pass(self):
        self.assertTrue(promotion_window_is_satisfied([False, True, True, True]))

    def test_recent_failure_resets_window(self):
        self.assertEqual(1, consecutive_healthy_samples([True, True, False, True]))
        self.assertFalse(promotion_window_is_satisfied([True, True, False, True]))


if __name__ == "__main__":
    unittest.main()
