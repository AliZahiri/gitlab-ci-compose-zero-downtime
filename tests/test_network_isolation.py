import unittest

from compose_zero_downtime.network_isolation import compose_network_isolation_is_safe, compose_network_isolation_violations


class ComposeNetworkIsolationGateTests(unittest.TestCase):
    def test_proxy_edge_and_private_workloads_pass(self):
        services = {"nginx": {"role": "proxy", "networks": ["edge", "backend"], "published_ports": [443]}, "app-blue": {"role": "workload", "networks": ["backend"]}, "db": {"role": "data", "networks": ["backend"]}}
        self.assertTrue(compose_network_isolation_is_safe(services))

    def test_public_workload_data_port_and_disconnected_proxy_fail(self):
        services = {"nginx": {"role": "proxy", "networks": ["edge"]}, "app": {"role": "workload", "networks": ["edge", "backend"], "published_ports": [8080]}, "db": {"role": "data", "networks": ["backend"], "published_ports": [5432]}}
        violations = compose_network_isolation_violations(services)
        self.assertIn("service:nginx:proxy_must_join_public_and_private_networks", violations)
        self.assertIn("service:app:workload_must_be_private_only", violations)
        self.assertIn("service:app:workload_must_not_publish_ports", violations)
        self.assertIn("service:db:data_must_not_publish_ports", violations)

    def test_empty_services_and_invalid_network_policy_fail(self):
        self.assertEqual(("at_least_one_service_is_required",), compose_network_isolation_violations({}))
        with self.assertRaises(ValueError):
            compose_network_isolation_violations({}, public_network="same", private_network="same")


if __name__ == "__main__":
    unittest.main()
