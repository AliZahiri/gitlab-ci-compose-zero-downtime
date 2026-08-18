import unittest
from datetime import datetime, timezone

from compose_zero_downtime.artifact_age_policy import artifact_age_violations, artifact_is_current


class ArtifactAgePolicyTests(unittest.TestCase):
    def test_recent_immutable_artifact_passes(self):
        artifact = {"built_at": "2026-08-18T05:55:00Z", "digest": "sha256:" + "a" * 64}
        self.assertTrue(artifact_is_current(artifact, now=datetime(2026, 8, 18, 6, 0, tzinfo=timezone.utc)))

    def test_stale_mutable_and_naive_artifact_fails(self):
        artifact = {"built_at": "2026-08-17T00:00:00", "digest": "latest"}
        violations = artifact_age_violations(artifact, now=datetime(2026, 8, 18, 6, 0, tzinfo=timezone.utc))
        self.assertIn("built_at_must_be_timezone_aware", violations)
        self.assertIn("artifact_digest_must_be_immutable", violations)


if __name__ == "__main__":
    unittest.main()
