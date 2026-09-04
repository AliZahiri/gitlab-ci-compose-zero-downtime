import unittest
from datetime import datetime, timezone

from compose_zero_downtime.restart_stability import candidate_restart_stability_is_safe, restart_stability_violations


NOW = datetime(2026, 9, 4, 6, 0, tzinfo=timezone.utc)
POLICY = {"expected_containers": frozenset({"app", "worker"}), "now": NOW}


class CandidateRestartStabilityEvidenceTests(unittest.TestCase):
    def test_stable_running_candidate_passes(self):
        containers = {name: {"baseline_restart_count": 1, "current_restart_count": 1, "running": True, "oom_killed": False} for name in ("app", "worker")}
        self.assertTrue(candidate_restart_stability_is_safe({"containers": containers, "observed_at": "2026-09-04T05:59:00Z"}, **POLICY))

    def test_restart_oom_and_missing_container_fail(self):
        evidence = {"containers": {"app": {"baseline_restart_count": 0, "current_restart_count": 2, "running": False, "oom_killed": True}}, "observed_at": "2026-09-04T05:59:00Z"}
        violations = restart_stability_violations(evidence, **POLICY)
        self.assertIn("observed_container_set_does_not_match_expected", violations)
        self.assertIn("app:restart_increase_exceeds_budget", violations)
        self.assertIn("app:must_not_be_oom_killed", violations)
        self.assertIn("worker:stability_state_is_required", violations)

    def test_stale_evidence_and_invalid_policy_fail(self):
        evidence = {"containers": {}, "observed_at": "2026-09-04T04:00:00Z"}
        self.assertIn("restart_stability_observation_is_invalid_stale_or_future_dated", restart_stability_violations(evidence, **POLICY))
        with self.assertRaises(ValueError):
            restart_stability_violations({}, **{**POLICY, "maximum_restart_increase": -1})
