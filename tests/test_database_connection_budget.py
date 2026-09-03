import unittest

from compose_zero_downtime.database_connection_budget import database_connection_budget_is_safe, database_connection_budget_violations


class DatabaseConnectionBudgetGateTests(unittest.TestCase):
    def test_dual_color_pools_within_reserved_budget_pass(self):
        colors = {"blue": {"replicas": 2, "pool_size": 20, "pooling_enabled": True}, "green": {"replicas": 2, "pool_size": 20, "pooling_enabled": True}}
        self.assertTrue(database_connection_budget_is_safe(colors, database_max_connections=120, reserved_connections=20))

    def test_missing_unpooled_and_overcommitted_colors_fail(self):
        colors = {"blue": {"replicas": 3, "pool_size": 40, "pooling_enabled": False}}
        violations = database_connection_budget_violations(colors, database_max_connections=100, reserved_connections=10)
        self.assertIn("blue:connection_pooling_must_be_enabled", violations)
        self.assertIn("green:connection_plan_is_required", violations)
        self.assertIn("dual_color_connection_demand_exceeds_database_budget", violations)

    def test_invalid_budget_fails(self):
        with self.assertRaises(ValueError):
            database_connection_budget_violations({}, database_max_connections=10, reserved_connections=10)
