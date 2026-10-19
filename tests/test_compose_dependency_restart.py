import unittest

from scripts.validate_compose_dependency_restart import (
    compose_dependency_restart_contract_is_safe,
    compose_dependency_restart_violations,
)


class ComposeDependencyRestartContractTests(unittest.TestCase):
    def test_health_gated_required_restart_dependency_passes(self):
        services = {"api_green": {"depends_on": {"database": {"condition": "service_healthy", "restart": True, "required": True}}}, "database": {}}
        self.assertTrue(compose_dependency_restart_contract_is_safe(services))

    def test_short_form_missing_service_and_unsafe_contract_fail(self):
        services = {"api_green": {"depends_on": {"database": {"condition": "service_started", "restart": False, "required": False}, "cache": {}}}, "database": {}}
        violations = compose_dependency_restart_violations(services)
        self.assertIn("api_green:database:dependency_must_be_health_gated", violations)
        self.assertIn("api_green:database:dependency_restart_must_be_enabled", violations)
        self.assertIn("api_green:cache:dependency_is_not_declared", violations)

    def test_invalid_service_collection_fails(self):
        self.assertEqual(("services_must_be_a_non_empty_object",), compose_dependency_restart_violations([]))
