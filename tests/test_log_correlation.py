import unittest

from compose_zero_downtime.log_correlation import deployment_log_correlation_violations, deployment_logs_are_correlated


class DeploymentLogCorrelationEvidenceTests(unittest.TestCase):
    def test_complete_ordered_shared_identity_passes(self):
        events = [{"stage": stage, "release_id": "rel-42", "correlation_id": "deploy-42", "observed_at": f"2026-09-02T04:0{index}:00Z", "status": "succeeded"} for index, stage in enumerate(("deploy", "proxy_switch", "smoke_test"))]
        self.assertTrue(deployment_logs_are_correlated(events))

    def test_missing_stage_mixed_identity_and_failure_fail(self):
        events = [{"stage": "deploy", "release_id": "rel-1", "correlation_id": "a", "observed_at": "2026-09-02T04:02:00Z", "status": "failed"}, {"stage": "proxy_switch", "release_id": "rel-2", "correlation_id": "b", "observed_at": "2026-09-02T04:01:00Z", "status": "succeeded"}]
        violations = deployment_log_correlation_violations(events)
        self.assertIn("required_stage_smoke_test_is_missing", violations)
        self.assertIn("events_must_share_one_release_id", violations)
        self.assertIn("events_must_share_one_correlation_id", violations)
        self.assertIn("event_timestamps_must_be_ordered", violations)
