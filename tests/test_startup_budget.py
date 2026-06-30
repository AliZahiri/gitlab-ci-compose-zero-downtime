import unittest

from compose_zero_downtime.startup_budget import startup_budget_is_safe, startup_budget_warnings


class StartupBudgetTests(unittest.TestCase):
    def test_safe_budget_passes(self):
        self.assertTrue(startup_budget_is_safe(attempts=30, interval_seconds=2))

    def test_oversized_budget_is_reported(self):
        self.assertIn("startup_budget_exceeds_max_seconds", startup_budget_warnings(attempts=100, interval_seconds=5))


if __name__ == "__main__":
    unittest.main()
