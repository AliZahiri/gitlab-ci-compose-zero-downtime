import unittest
from datetime import datetime, timezone

from compose_zero_downtime.freeze_evidence import deployment_has_freeze_clearance, freeze_evidence_violations


NOW = datetime(2026, 8, 19, 6, 0, tzinfo=timezone.utc)


class FreezeEvidenceTests(unittest.TestCase):
    def test_fresh_standard_deployment_outside_freeze_passes(self):
        evidence = {"freeze_active": False, "deployment_type": "standard", "observed_at": "2026-08-19T05:55:00Z"}
        self.assertTrue(deployment_has_freeze_clearance(evidence, now=NOW))

    def test_active_freeze_requires_approved_emergency_evidence(self):
        evidence = {"freeze_active": True, "deployment_type": "standard", "observed_at": "2026-08-19T05:00:00Z"}
        violations = freeze_evidence_violations(evidence, now=NOW)
        self.assertIn("active_freeze_requires_emergency_deployment", violations)
        self.assertIn("freeze_evidence_is_not_fresh", violations)
        emergency = {**evidence, "deployment_type": "emergency", "approval_reference": "CHG-77", "approved_by": "release-manager", "emergency_reason": "critical recovery", "observed_at": "2026-08-19T05:55:00Z"}
        self.assertTrue(deployment_has_freeze_clearance(emergency, now=NOW))

    def test_invalid_policy_and_naive_clock_fail(self):
        with self.assertRaises(ValueError):
            freeze_evidence_violations({}, now=NOW, maximum_age_seconds=0)
        with self.assertRaises(ValueError):
            freeze_evidence_violations({}, now=datetime(2026, 8, 19, 6, 0))
