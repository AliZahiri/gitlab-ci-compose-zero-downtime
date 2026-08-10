import unittest

from compose_zero_downtime.deployment_timeout_budget import deployment_timeout_is_within_budget, deployment_timeout_violations


class DeploymentTimeoutBudgetGateTests(unittest.TestCase):
    def test_stage_and_total_budget_pass(self):
        budgets = {"pull": 60, "startup": 120, "health": 90, "promotion": 30, "total": 330}
        observations = {"pull": 20, "startup": 80, "health": 45, "promotion": 10}

        self.assertTrue(deployment_timeout_is_within_budget(budgets, observations))

    def test_invalid_stage_and_total_budget_fail_together(self):
        budgets = {"pull": 60, "startup": 0, "health": 90, "promotion": 30, "total": 100}
        observations = {"pull": 70, "startup": 1, "health": -1, "promotion": 30}

        violations = deployment_timeout_violations(budgets, observations)

        self.assertIn("pull:timeout_budget_exceeded", violations)
        self.assertIn("startup:budget_must_be_positive", violations)
        self.assertIn("health:observation_must_be_non_negative", violations)
        self.assertIn("total:budget_must_cover_declared_stages", violations)


if __name__ == "__main__":
    unittest.main()
