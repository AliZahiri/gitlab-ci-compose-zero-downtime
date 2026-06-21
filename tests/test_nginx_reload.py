import unittest

from compose_zero_downtime.nginx_reload import nginx_reload_commands, reload_is_preferred_over_restart


class NginxReloadTests(unittest.TestCase):
    def test_reload_plan_validates_config_before_reload(self):
        reload_command, fallback_command = nginx_reload_commands(validate_config=True)

        self.assertIn("-t", reload_command)
        self.assertIn("reload", reload_command)
        self.assertIn("restart", fallback_command)

    def test_reload_is_preferred_over_restart(self):
        self.assertTrue(reload_is_preferred_over_restart(nginx_reload_commands()))


if __name__ == "__main__":
    unittest.main()
