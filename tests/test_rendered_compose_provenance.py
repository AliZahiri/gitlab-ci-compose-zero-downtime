import unittest
from datetime import datetime, timezone

from compose_zero_downtime.rendered_compose_provenance import rendered_compose_provenance_is_verified, rendered_compose_provenance_violations


NOW = datetime(2026, 9, 4, 6, 0, tzinfo=timezone.utc)
DIGEST = "sha256:" + "a" * 64
POLICY = {"expected_services": frozenset({"app", "worker"}), "now": NOW}


class RenderedComposeProvenanceGateTests(unittest.TestCase):
    def test_matching_fresh_rendered_plan_passes(self):
        evidence = {"reviewed_compose_sha256": DIGEST, "deployed_compose_sha256": DIGEST, "reviewed_environment_contract_sha256": DIGEST, "deployed_environment_contract_sha256": DIGEST, "services": ["app", "worker"], "observed_at": "2026-09-04T05:55:00Z"}
        self.assertTrue(rendered_compose_provenance_is_verified(evidence, **POLICY))

    def test_config_drift_extra_service_and_stale_evidence_fail(self):
        evidence = {"reviewed_compose_sha256": DIGEST, "deployed_compose_sha256": "sha256:" + "b" * 64, "reviewed_environment_contract_sha256": DIGEST, "deployed_environment_contract_sha256": "bad", "services": ["app", "worker", "debug"], "observed_at": "2026-09-04T04:00:00Z"}
        violations = rendered_compose_provenance_violations(evidence, **POLICY)
        self.assertIn("compose_digest_does_not_match_reviewed_plan", violations)
        self.assertIn("deployed_environment_contract_sha256_must_be_a_digest", violations)
        self.assertIn("rendered_service_set_does_not_match_expected", violations)
        self.assertIn("compose_provenance_observation_is_invalid_stale_or_future_dated", violations)

    def test_invalid_policy_and_shape_fail(self):
        self.assertEqual(("compose_provenance_evidence_must_be_an_object",), rendered_compose_provenance_violations([], **POLICY))
        with self.assertRaises(ValueError):
            rendered_compose_provenance_violations({}, expected_services=frozenset(), now=NOW)
