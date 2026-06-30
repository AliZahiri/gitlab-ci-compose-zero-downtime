import unittest

from compose_zero_downtime.deploy_audit import deploy_audit_event_is_complete, missing_audit_fields


class DeployAuditTests(unittest.TestCase):
    def test_complete_event_passes(self):
        event = {"actor": "ci", "commit_sha": "abcdef1", "image": "api:v1.0.0", "target_color": "green", "result": "success"}

        self.assertTrue(deploy_audit_event_is_complete(event))

    def test_missing_event_fields_are_reported(self):
        self.assertIn("image", missing_audit_fields({"actor": "ci"}))


if __name__ == "__main__":
    unittest.main()
