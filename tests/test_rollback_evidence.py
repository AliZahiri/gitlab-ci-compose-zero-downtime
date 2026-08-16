import unittest

from compose_zero_downtime.rollback_evidence import rollback_evidence_is_actionable, rollback_evidence_violations


class RollbackEvidenceContractTests(unittest.TestCase):
    def test_actionable_rollback_evidence_passes(self):
        self.assertTrue(rollback_evidence_is_actionable({"active_color": "green", "rollback_image_digest": "sha256:" + "b" * 64, "decision_at": "2026-08-16T12:00:00Z", "health_reason": "candidate probe failed"}))

    def test_incomplete_rollback_evidence_fails(self):
        violations = rollback_evidence_violations({"active_color": "red", "rollback_image_digest": "latest", "decision_at": "2026-08-16T12:00:00", "health_reason": ""})
        self.assertEqual(len(violations), 4)


if __name__ == "__main__":
    unittest.main()
