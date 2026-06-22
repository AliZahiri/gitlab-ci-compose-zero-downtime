import unittest

from compose_zero_downtime.nginx_reload import nginx_reload_commands, reload_is_preferred_over_restart


class NginxReloadTests(unittest.TestCase):
    def test_reload_plan_validates_config_before_reload(self):
        reload_commands, fallback_command = nginx_reload_commands(validate_config=True)

        self.assertEqual(reload_commands[0], ["nginx", "-t"])
        self.assertEqual(reload_commands[1], ["nginx", "-s", "reload"])
        self.assertIn("restart", fallback_command)

    def test_reload_plan_can_skip_config_validation_for_prevalidated_config(self):
        reload_commands, _ = nginx_reload_commands(validate_config=False)

        self.assertEqual(reload_commands, [["nginx", "-s", "reload"]])

    def test_reload_is_preferred_over_restart(self):
        self.assertTrue(reload_is_preferred_over_restart(nginx_reload_commands()))


if __name__ == "__main__":
    unittest.main()
