import unittest

from compose_zero_downtime.sbom_attestation import sbom_attestation_is_valid, sbom_attestation_violations

DIGEST = "sha256:" + "a" * 64


class ReleaseSbomAttestationTests(unittest.TestCase):
    def test_signed_sbom_bound_to_release_passes(self):
        attestation = {"subject_digest": DIGEST, "sbom_digest": "sha256:" + "b" * 64, "format": "CycloneDX", "signature_verified": True, "generated_at": "2026-08-23T08:00:00Z"}
        self.assertTrue(sbom_attestation_is_valid(attestation, release_digest=DIGEST))

    def test_mismatched_unsigned_sbom_fails(self):
        violations = sbom_attestation_violations({"subject_digest": "sha256:" + "c" * 64, "sbom_digest": "bad", "format": "unknown", "signature_verified": False, "generated_at": "2026-08-23"}, release_digest=DIGEST)
        self.assertEqual(len(violations), 5)
