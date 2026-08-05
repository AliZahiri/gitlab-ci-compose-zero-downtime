import unittest

from compose_zero_downtime.dependency_health import dependency_health_violations, release_dependency_health_is_ready


class DependencyHealthContractTests(unittest.TestCase):
    def test_promoted_service_with_health_gated_dependencies_passes(self):
        services = {"api": {"healthcheck_enabled": True, "depends_on": {"db": {"condition": "service_healthy"}, "migrate": {"condition": "service_completed_successfully"}}}, "db": {"depends_on": {}}, "migrate": {"depends_on": {"db": {"condition": "service_healthy"}}}}
        self.assertTrue(release_dependency_health_is_ready(services, promoted_service="api"))

    def test_unhealthy_unknown_self_referential_and_started_dependencies_fail(self):
        services = {"api": {"healthcheck_enabled": False, "depends_on": {"db": {"condition": "service_started"}, "missing": {"condition": "service_healthy"}, "api": {"condition": "service_healthy"}}}, "db": {"depends_on": {}}}
        violations = dependency_health_violations(services, promoted_service="api")
        self.assertIn("service:api:healthcheck_must_be_enabled", violations)
        self.assertIn("service:api:dependency:db:service_started_is_not_allowed", violations)
        self.assertIn("service:api:dependency:missing:is_not_declared", violations)
        self.assertIn("service:api:cannot_depend_on_itself", violations)

    def test_cycles_and_invalid_policy_fail(self):
        services = {"api": {"healthcheck_enabled": True, "depends_on": {"worker": {"condition": "service_healthy"}}}, "worker": {"depends_on": {"api": {"condition": "service_healthy"}}}}
        self.assertIn("dependency_cycle_detected", dependency_health_violations(services, promoted_service="api"))
        with self.assertRaises(ValueError):
            dependency_health_violations(services, promoted_service="")


if __name__ == "__main__":
    unittest.main()
