import unittest

from scripts.compose_service_resource_contract import compose_service_resource_violations, compose_service_resources_are_ready


class ComposeServiceResourceContractTests(unittest.TestCase):
    def test_bounded_service_contract_passes(self):
        services = [{"name": "api-green", "cpu_limit": 1.0, "memory_limit_mib": 512, "restart": "on-failure", "readiness_timeout_seconds": 90}]
        self.assertTrue(compose_service_resources_are_ready(services))

    def test_duplicate_under_provisioned_and_unbounded_service_fails(self):
        services = [{"name": "api", "cpu_limit": 0, "memory_limit_mib": 32, "restart": "always", "readiness_timeout_seconds": 600}, {"name": "api", "cpu_limit": 1, "memory_limit_mib": 128, "restart": "on-failure", "readiness_timeout_seconds": 30}]
        violations = compose_service_resource_violations(services)
        self.assertIn("service_0:cpu_limit_must_be_positive", violations)
        self.assertIn("service_0:memory_limit_is_below_policy", violations)
        self.assertIn("service_0:restart_policy_is_not_approved", violations)
        self.assertIn("service_0:readiness_timeout_is_out_of_policy", violations)
        self.assertIn("service_1:name_must_be_unique", violations)

    def test_invalid_policy_fails(self):
        with self.assertRaises(ValueError):
            compose_service_resource_violations([], minimum_memory_mib=0)
