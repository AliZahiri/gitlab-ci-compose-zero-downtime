import unittest

from compose_zero_downtime.artifact_integrity import artifact_integrity_warnings, artifact_is_promotable


class ArtifactIntegrityTests(unittest.TestCase):
    def test_digest_pinned_artifact_is_promotable(self):
        artifact = {"image": "registry.example/app", "digest": "sha256:abc123", "build_id": "build-42", "source_revision": "deadbeef"}

        self.assertTrue(artifact_is_promotable(artifact))

    def test_mutable_digest_is_rejected(self):
        warnings = artifact_integrity_warnings({"image": "registry.example/app", "digest": "latest"})

        self.assertIn("build_id_is_required", warnings)
        self.assertIn("digest_must_use_sha256", warnings)


if __name__ == "__main__":
    unittest.main()
