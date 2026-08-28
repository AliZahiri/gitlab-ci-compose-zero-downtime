import unittest

from compose_zero_downtime.project_namespace import expected_project_name, project_namespace_is_isolated, project_namespace_violations


class ComposeProjectNamespaceContractTests(unittest.TestCase):
    def test_namespaced_stack_with_approved_shared_network_passes(self):
        evidence = {"stack": "payments", "environment": "staging", "project_name": "payments-staging", "resources": [{"kind": "container", "name": "payments-staging_app-blue"}, {"kind": "network", "name": "edge", "shared": True, "shared_resource_approved": True}]}
        self.assertTrue(project_namespace_is_isolated(evidence))
        self.assertEqual(expected_project_name("payments", "staging"), "payments-staging")

    def test_wrong_project_and_unnamespaced_resource_fail(self):
        evidence = {"stack": "payments", "environment": "prod", "project_name": "default", "resources": [{"kind": "volume", "name": "database"}]}
        violations = project_namespace_violations(evidence)
        self.assertIn("project_name_must_match_stack_and_environment", violations)
        self.assertIn("resource_0:name_must_use_project_namespace", violations)

    def test_duplicate_and_unapproved_shared_resources_fail(self):
        resource = {"kind": "network", "name": "edge", "shared": True}
        violations = project_namespace_violations({"stack": "api", "environment": "prod", "project_name": "api-prod", "resources": [resource, dict(resource)]})
        self.assertIn("resource_0:shared_resource_requires_approval", violations)
        self.assertIn("resource_1:identity_must_be_unique", violations)
