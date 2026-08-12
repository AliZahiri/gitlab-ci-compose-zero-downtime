import unittest

from compose_zero_downtime.bind_mount_safety import compose_bind_mount_violations, compose_bind_mounts_are_safe


class ComposeBindMountSafetyGateTests(unittest.TestCase):
    def test_approved_read_only_mount_passes(self):
        services = {"api": {"bind_mounts": [{"source": "/srv/app/config/runtime.yml", "target": "/app/config/runtime.yml", "read_only": True}]}}
        self.assertTrue(compose_bind_mounts_are_safe(services))

    def test_dangerous_unapproved_and_writable_mounts_fail(self):
        services = {"api": {"bind_mounts": [{"source": "/var/run/docker.sock", "target": "/var/run/docker.sock", "read_only": False}, {"source": "/tmp/config", "target": "relative", "read_only": True}]}}
        violations = compose_bind_mount_violations(services)
        self.assertIn("service:api:mount_0:source_is_not_permitted", violations)
        self.assertIn("service:api:mount_0:must_be_read_only", violations)
        self.assertIn("service:api:mount_1:source_must_be_under_an_allowed_root", violations)
        self.assertIn("service:api:mount_1:target_must_be_an_absolute_non_root_path", violations)

    def test_empty_manifest_and_invalid_root_policy_fail(self):
        self.assertEqual(("at_least_one_service_is_required",), compose_bind_mount_violations({}))
        with self.assertRaises(ValueError):
            compose_bind_mount_violations({"api": {"bind_mounts": []}}, allowed_source_roots=("/",))


if __name__ == "__main__":
    unittest.main()
