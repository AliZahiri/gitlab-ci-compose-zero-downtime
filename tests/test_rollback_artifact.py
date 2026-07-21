import unittest

from compose_zero_downtime.rollback_artifact import rollback_artifact_is_ready, rollback_artifact_warnings


class RollbackArtifactTests(unittest.TestCase):
    def test_available_verified_previous_digest_passes(self):
        previous = "sha256:" + "a" * 64
        candidate = "sha256:" + "b" * 64
        self.assertTrue(rollback_artifact_is_ready({"previous_digest": previous, "candidate_digest": candidate, "available_digests": [previous], "verified_digests": [previous]}))

    def test_mutable_or_missing_artifact_is_rejected(self):
        warnings = rollback_artifact_warnings({"previous_digest": "latest", "candidate_digest": "sha256:" + "b" * 64, "available_digests": [], "verified_digests": []})
        self.assertIn("previous_digest_is_not_immutable", warnings)
        self.assertIn("previous_artifact_is_unavailable", warnings)

    def test_candidate_cannot_be_its_own_rollback(self):
        digest = "sha256:" + "c" * 64
        warnings = rollback_artifact_warnings({"previous_digest": digest, "candidate_digest": digest, "available_digests": [digest], "verified_digests": [digest]})
        self.assertIn("previous_digest_matches_candidate", warnings)


if __name__ == "__main__":
    unittest.main()
