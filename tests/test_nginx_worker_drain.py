import unittest

from compose_zero_downtime.nginx_worker_drain import nginx_worker_drain_violations, nginx_workers_are_drained


class NginxWorkerDrainEvidenceTests(unittest.TestCase):
    def test_monotonic_healthy_drain_to_zero_passes(self):
        samples = [{"elapsed_seconds": 0, "old_worker_active_connections": 8, "candidate_upstream_healthy": True, "rollback_ready": True}, {"elapsed_seconds": 20, "old_worker_active_connections": 2, "candidate_upstream_healthy": True, "rollback_ready": True}, {"elapsed_seconds": 30, "old_worker_active_connections": 0, "candidate_upstream_healthy": True, "rollback_ready": True}]
        self.assertTrue(nginx_workers_are_drained(samples))

    def test_regression_unhealthy_candidate_and_timeout_fail(self):
        samples = [{"elapsed_seconds": 0, "old_worker_active_connections": 2, "candidate_upstream_healthy": True, "rollback_ready": True}, {"elapsed_seconds": 90, "old_worker_active_connections": 3, "candidate_upstream_healthy": False, "rollback_ready": False}]
        violations = nginx_worker_drain_violations(samples)
        self.assertIn("old_worker_connections_must_not_increase", violations)
        self.assertIn("old_worker_connections_must_reach_zero", violations)
        self.assertIn("worker_drain_budget_exceeded", violations)
        self.assertIn("sample_1:rollback_must_remain_ready", violations)

    def test_invalid_policy_fails(self):
        with self.assertRaises(ValueError):
            nginx_worker_drain_violations([], maximum_drain_seconds=0)
