import unittest
from datetime import datetime, timezone

from compose_zero_downtime.release_health_evidence import release_health_evidence_is_fresh, release_health_evidence_violations


class ReleaseHealthEvidenceFreshnessGateTests(unittest.TestCase):
    now = datetime(2026, 8, 17, 4, 0, tzinfo=timezone.utc)

    def test_recent_healthy_candidate_passes(self):
        self.assertTrue(release_health_evidence_is_fresh({"observed_at": "2026-08-17T03:58:00Z", "candidate_color": "green", "healthy": True}, now=self.now))

    def test_stale_invalid_and_unhealthy_evidence_fails(self):
        violations = release_health_evidence_violations({"observed_at": "2026-08-17T03:00:00Z", "candidate_color": "red", "healthy": False}, now=self.now)
        self.assertEqual(violations, ("health_evidence_is_outside_age_budget", "candidate_color_must_be_blue_or_green", "candidate_health_must_pass"))


if __name__ == "__main__":
    unittest.main()
