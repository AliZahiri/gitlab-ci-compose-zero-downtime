import unittest

from compose_zero_downtime.promotion_observation_order import promotion_observation_order_is_safe


class PromotionObservationOrderTests(unittest.TestCase):
    def test_health_switch_and_observation_order_passes(self):
        self.assertTrue(promotion_observation_order_is_safe(["candidate_healthy", "traffic_switched", "post_switch_healthy"]))

    def test_switch_before_health_fails(self):
        self.assertFalse(promotion_observation_order_is_safe(["traffic_switched", "candidate_healthy"]))
