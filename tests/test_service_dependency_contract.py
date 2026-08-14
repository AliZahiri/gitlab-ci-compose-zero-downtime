import unittest

from compose_zero_downtime.service_dependency_contract import service_dependencies_are_safe, service_dependency_contract_violations


class ServiceDependencyContractTests(unittest.TestCase):
    def test_health_gated_dependency_passes(self):
        services = [{"name": "api-green", "critical_dependencies": [{"service": "database", "condition": "service_healthy", "restart": True}]}]
        self.assertTrue(service_dependencies_are_safe(services))

    def test_duplicate_and_unsafe_dependencies_fail(self):
        services = [{"name": "api", "critical_dependencies": [{"service": "db", "condition": "service_started", "restart": False}]}, {"name": "api", "critical_dependencies": "db"}]
        violations = service_dependency_contract_violations(services)
        self.assertIn("service_0:dependency_0:must_wait_for_health", violations)
        self.assertIn("service_0:dependency_0:restart_propagation_is_required", violations)
        self.assertIn("service_1:name_must_be_unique", violations)
        self.assertIn("service_1:critical_dependencies_must_be_a_list", violations)


if __name__ == "__main__":
    unittest.main()
