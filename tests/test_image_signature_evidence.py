import unittest

from compose_zero_downtime.image_signature_evidence import image_signature_evidence_is_safe, image_signature_evidence_violations


class ReleaseImageSignatureEvidenceGateTests(unittest.TestCase):
    def test_trusted_verified_image_evidence_passes(self):
        evidence = {"image_digest": "sha256:" + "a" * 64, "signer": "release-ci", "signature_verified": True, "verified_at": "2026-08-11T08:00:00Z"}
        self.assertTrue(image_signature_evidence_is_safe(evidence, trusted_signers={"release-ci"}))

    def test_untrusted_unverified_and_mutable_evidence_fails(self):
        violations = image_signature_evidence_violations({"image_digest": "app:latest", "signer": "unknown", "signature_verified": False, "verified_at": "2026-08-11T08:00:00"}, trusted_signers={"release-ci"})
        self.assertIn("image_digest_must_be_immutable", violations)
        self.assertIn("signer_must_be_trusted", violations)
        self.assertIn("signature_must_be_verified", violations)
        self.assertIn("verified_at_must_be_timezone_aware", violations)


if __name__ == "__main__":
    unittest.main()
