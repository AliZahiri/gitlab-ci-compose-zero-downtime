import unittest

from compose_zero_downtime.candidate_runtime_identity import candidate_runtime_identity_matches, candidate_runtime_identity_violations


class PromotionCandidateRuntimeIdentityTests(unittest.TestCase):
    def test_matching_running_candidate_passes(self):
        expected = {"image_digest": "sha256:" + "a" * 64, "config_sha256": "b" * 64}
        observed = {**expected, "container_running": True, "observed_at": "2026-08-26T08:00:00Z"}
        self.assertTrue(candidate_runtime_identity_matches(expected, observed))

    def test_drifted_stopped_candidate_fails(self):
        expected = {"image_digest": "sha256:" + "a" * 64, "config_sha256": "b" * 64}
        violations = candidate_runtime_identity_violations(expected, {"image_digest": "sha256:" + "c" * 64, "config_sha256": "d" * 64, "container_running": False, "observed_at": "naive"})
        self.assertEqual(len(violations), 4)
