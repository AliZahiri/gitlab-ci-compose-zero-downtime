import unittest

from compose_zero_downtime.promotion_approval import promotion_approval_violations, promotion_is_approved


class PromotionApprovalEvidenceGateTests(unittest.TestCase):
    def test_complete_approval_evidence_passes(self):
        evidence = {"release_id": "2026.08.20-1", "candidate_digest": "sha256:" + "a" * 64, "change_ticket": "OPS-42", "approved_by": "release-manager", "approved_at": "2026-08-20T12:00:00Z", "change_window_open": True, "rollback_ready": True}
        self.assertTrue(promotion_is_approved(evidence))

    def test_missing_or_unverifiable_approval_fails(self):
        violations = promotion_approval_violations({"release_id": "", "candidate_digest": "latest", "change_ticket": "42", "approved_by": "", "approved_at": "2026-08-20T12:00:00", "change_window_open": False, "rollback_ready": False})
        self.assertEqual(violations, ("release_id_is_required", "candidate_digest_must_be_immutable", "change_ticket_is_invalid", "approved_by_is_required", "approved_at_must_be_timezone_aware", "change_window_must_be_open", "rollback_must_be_ready"))
