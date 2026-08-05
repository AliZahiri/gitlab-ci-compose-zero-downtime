import unittest

from compose_zero_downtime.secret_references import compose_secret_reference_violations, compose_secret_references_are_safe


class ComposeSecretReferenceGateTests(unittest.TestCase):
    def test_variable_and_docker_secret_references_pass(self):
        services = {"api": {"environment": {"DB_PASSWORD_FILE": "/run/secrets/db_password", "API_TOKEN": "${API_TOKEN}", "APP_PORT": "8080"}}}
        self.assertTrue(compose_secret_references_are_safe(services))

    def test_embedded_values_and_invalid_secret_paths_fail(self):
        services = {"api": {"environment": {"DB_PASSWORD": "not-a-reference", "API_TOKEN_FILE": "/tmp/token", "PRIVATE_KEY_FILE": "/run/secrets/../private"}}}
        violations = compose_secret_reference_violations(services)
        self.assertIn("service:api:environment:DB_PASSWORD:must_not_embed_sensitive_value", violations)
        self.assertIn("service:api:environment:API_TOKEN_FILE:must_reference_secret_mount", violations)
        self.assertIn("service:api:environment:PRIVATE_KEY_FILE:must_reference_secret_mount", violations)

    def test_invalid_manifest_and_policy_fail(self):
        self.assertEqual(("at_least_one_service_is_required",), compose_secret_reference_violations({}))
        with self.assertRaises(ValueError):
            compose_secret_reference_violations({"api": {}}, secret_mount_root="run/secrets")


if __name__ == "__main__":
    unittest.main()
