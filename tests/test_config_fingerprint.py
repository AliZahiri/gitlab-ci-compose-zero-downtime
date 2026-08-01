import unittest

from compose_zero_downtime.config_fingerprint import config_fingerprint_violations, release_config_is_pinned


DIGEST_A = "a" * 64
DIGEST_B = "b" * 64


class ReleaseConfigFingerprintGateTests(unittest.TestCase):
    def test_matching_planned_observed_and_available_rollback_fingerprints_pass(self):
        evidence = {name: {"planned_sha256": DIGEST_A, "observed_sha256": DIGEST_A, "rollback_sha256": DIGEST_B} for name in ("compose", "proxy", "environment")}
        self.assertTrue(release_config_is_pinned(evidence))

    def test_missing_component_drift_and_invalid_rollback_are_reported(self):
        evidence = {"compose": {"planned_sha256": DIGEST_A, "observed_sha256": DIGEST_B, "rollback_sha256": "latest"}}
        violations = config_fingerprint_violations(evidence)
        self.assertIn("component:compose:planned_and_observed_fingerprints_differ", violations)
        self.assertIn("component:compose:rollback_fingerprint_is_invalid", violations)
        self.assertIn("component:proxy:fingerprint_evidence_is_required", violations)

    def test_invalid_required_component_policy_fails(self):
        with self.assertRaises(ValueError):
            config_fingerprint_violations({}, required_components=("proxy", "proxy"))


if __name__ == "__main__":
    unittest.main()
