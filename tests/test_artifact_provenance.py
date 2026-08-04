import unittest

from compose_zero_downtime.artifact_provenance import artifact_provenance_violations, release_artifacts_have_provenance


DIGEST = "sha256:" + "a" * 64


class ReleaseArtifactProvenanceGateTests(unittest.TestCase):
    def test_verified_matching_image_sbom_and_provenance_pass(self):
        artifact = {"image": "registry.example/app", "image_digest": DIGEST, "sbom_subject_digest": DIGEST, "provenance_subject_digest": DIGEST, "signature_verified": True}
        self.assertTrue(release_artifacts_have_provenance([artifact]))

    def test_duplicate_malformed_mismatched_and_unsigned_artifacts_fail(self):
        artifact = {"image": "app", "image_digest": DIGEST, "sbom_subject_digest": "sha256:" + "b" * 64, "provenance_subject_digest": "bad", "signature_verified": False}
        violations = artifact_provenance_violations([artifact, artifact])
        self.assertIn("artifact_0:sbom_subject_digest_mismatch", violations)
        self.assertIn("artifact_0:provenance_subject_digest_must_be_an_oci_sha256_digest", violations)
        self.assertIn("artifact_0:signature_must_be_verified", violations)
        self.assertIn("artifact_1:image_must_be_unique", violations)

    def test_empty_artifact_set_fails(self):
        self.assertEqual(("at_least_one_release_artifact_is_required",), artifact_provenance_violations([]))


if __name__ == "__main__":
    unittest.main()
