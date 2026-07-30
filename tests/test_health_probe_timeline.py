import unittest
from datetime import datetime, timezone

from compose_zero_downtime.health_probe_timeline import health_probe_timeline_is_promotable, health_probe_timeline_violations


NOW = datetime(2026, 7, 30, 8, 0, tzinfo=timezone.utc)


class HealthProbeTimelineGateTests(unittest.TestCase):
    def test_recent_ordered_consecutive_health_samples_pass(self):
        samples = [{"observed_at": "2026-07-30T07:59:20Z", "healthy": True}, {"observed_at": "2026-07-30T07:59:40Z", "healthy": True}, {"observed_at": "2026-07-30T08:00:00Z", "healthy": True}]
        self.assertTrue(health_probe_timeline_is_promotable(samples=samples, now=NOW))

    def test_stale_gapped_and_unhealthy_timeline_reports_all_failures(self):
        samples = [{"observed_at": "2026-07-30T07:55:00Z", "healthy": True}, {"observed_at": "2026-07-30T07:57:00Z", "healthy": False}]
        violations = health_probe_timeline_violations(samples, now=NOW, required_consecutive=2, maximum_interval_seconds=30, maximum_age_seconds=60)
        self.assertIn("sample_1:observation_interval_exceeds_maximum", violations)
        self.assertIn("latest_health_observation_is_stale", violations)
        self.assertIn("consecutive_healthy_sample_requirement_not_met", violations)

    def test_invalid_timestamp_shape_and_policy_values_fail(self):
        violations = health_probe_timeline_violations([{"observed_at": "2026-07-30T08:00:00", "healthy": "yes"}], now=NOW)
        self.assertIn("sample_0:observed_at_must_be_timezone_aware", violations)
        self.assertIn("sample_0:healthy_must_be_boolean", violations)
        with self.assertRaises(ValueError):
            health_probe_timeline_violations([], now=NOW, required_consecutive=0)


if __name__ == "__main__":
    unittest.main()
