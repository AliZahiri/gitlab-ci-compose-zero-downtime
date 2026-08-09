import unittest

from compose_zero_downtime.shutdown_budget import shutdown_budget_is_safe, shutdown_budget_violations


class ContainerShutdownBudgetGateTests(unittest.TestCase):
    def test_sigterm_with_drain_termination_and_margin_passes(self):
        services = [{"service": "app-blue", "stop_signal": "SIGTERM", "drain_seconds": 10, "termination_seconds": 15, "stop_grace_period_seconds": 30}]
        self.assertTrue(shutdown_budget_is_safe(services))

    def test_duplicate_wrong_signal_and_short_grace_fail(self):
        services = [{"service": "app", "stop_signal": "SIGKILL", "drain_seconds": 10, "termination_seconds": 15, "stop_grace_period_seconds": 20}, {"service": "app", "stop_signal": "SIGTERM", "drain_seconds": -1, "termination_seconds": 1, "stop_grace_period_seconds": 5}]
        violations = shutdown_budget_violations(services)
        self.assertIn("service_0:stop_signal_must_be_sigterm", violations)
        self.assertIn("service_0:stop_grace_period_below_shutdown_budget", violations)
        self.assertIn("service_1:name_must_be_unique", violations)
        self.assertIn("service_1:drain_seconds_must_be_finite_and_non_negative", violations)

    def test_empty_input_and_invalid_margin_fail(self):
        self.assertEqual(("at_least_one_shutdown_observation_is_required",), shutdown_budget_violations([]))
        with self.assertRaises(ValueError):
            shutdown_budget_violations([], safety_margin_seconds=-1)


if __name__ == "__main__":
    unittest.main()
