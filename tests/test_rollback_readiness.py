import unittest

from compose_zero_downtime.rollback_readiness import rollback_is_ready, rollback_readiness_warnings


class RollbackReadinessTests(unittest.TestCase):
    def test_healthy_previous_color_is_ready(self):
        self.assertTrue(rollback_is_ready({"previous_color": "blue", "previous_color_healthy": True, "proxy_switch_ready": True}))

    def test_missing_proxy_readiness_blocks_rollback(self):
        warnings = rollback_readiness_warnings({"previous_color": "blue", "previous_color_healthy": True})

        self.assertIn("proxy_switch_is_not_ready", warnings)


if __name__ == "__main__":
    unittest.main()
