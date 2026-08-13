import unittest

from compose_zero_downtime.release_manifest import release_manifest_is_complete, release_manifest_violations


class ReleaseManifestCompletenessGateTests(unittest.TestCase):
    def test_complete_immutable_manifest_passes(self):
        manifest = {"release_id": "20260813.1", "image_digest": "sha256:" + "a" * 64, "source_revision": "b" * 40, "config_sha256": "c" * 64, "created_at": "2026-08-13T06:00:00Z"}
        self.assertTrue(release_manifest_is_complete(manifest))

    def test_incomplete_mutable_manifest_fails(self):
        violations = release_manifest_violations({"release_id": "", "image_digest": "app:latest", "source_revision": "short", "config_sha256": "bad", "created_at": "2026-08-13T06:00:00"})
        self.assertIn("release_id_is_required", violations)
        self.assertIn("image_digest_must_be_immutable", violations)
        self.assertIn("source_revision_must_be_full_sha", violations)
        self.assertIn("config_sha256_is_invalid", violations)
        self.assertIn("created_at_must_be_timezone_aware", violations)


if __name__ == "__main__":
    unittest.main()
