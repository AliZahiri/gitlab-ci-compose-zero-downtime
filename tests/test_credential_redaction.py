import unittest

from compose_zero_downtime.credential_redaction import credential_redaction_violations, deployment_artifact_is_redacted


class DeploymentCredentialRedactionTests(unittest.TestCase):
    def test_complete_clean_scan_passes(self):
        evidence = {"artifact_id": "sha256:plan", "scanner_version": "patterns-v2", "scan_completed": True, "covered_categories": ["token", "password", "authorization", "private_key"], "exposed_finding_ids": []}
        self.assertTrue(deployment_artifact_is_redacted(evidence))

    def test_incomplete_coverage_and_exposed_finding_fail(self):
        evidence = {"artifact_id": "plan-1", "scanner_version": "v1", "scan_completed": False, "covered_categories": ["token"], "exposed_finding_ids": ["finding-7"]}
        violations = credential_redaction_violations(evidence)
        self.assertIn("credential_scan_must_complete", violations)
        self.assertIn("required_sensitive_categories_are_not_covered", violations)
        self.assertIn("unredacted_credentials_detected", violations)
