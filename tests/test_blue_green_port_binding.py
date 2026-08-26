import unittest

from compose_zero_downtime.blue_green_port_binding import (
    blue_green_port_binding_violations,
    blue_green_port_bindings_are_safe,
)


class BlueGreenPortBindingContractTests(unittest.TestCase):
    def test_distinct_loopback_bindings_pass(self):
        bindings = [
            {"color": "blue", "host": "127.0.0.1", "port": 18081},
            {"color": "green", "host": "::1", "port": 18082},
        ]

        self.assertTrue(blue_green_port_bindings_are_safe(bindings))

    def test_duplicate_color_port_and_public_host_fail(self):
        bindings = [
            {"color": "blue", "host": "0.0.0.0", "port": 8080},
            {"color": "blue", "host": "127.0.0.1", "port": 8080},
        ]
        violations = blue_green_port_binding_violations(bindings)

        self.assertIn("binding_0:host_must_be_a_loopback_address", violations)
        self.assertIn("binding_1:color_must_be_unique", violations)
        self.assertIn("binding_1:port_must_be_unique", violations)
        self.assertIn("green_binding_is_required", violations)


if __name__ == "__main__":
    unittest.main()
