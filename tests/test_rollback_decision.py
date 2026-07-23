import unittest

from compose_zero_downtime.rollback_decision import rollback_is_required, rollback_reasons


class RollbackDecisionTests(unittest.TestCase):
    def test_healthy_release_within_budget_stays_promoted(self):
        self.assertFalse(rollback_is_required(healthy=True, error_rate=0.01, maximum_error_rate=0.02, consecutive_failures=0, failure_threshold=3))

    def test_independent_failure_signals_request_rollback(self):
        reasons = rollback_reasons(healthy=False, error_rate=0.03, maximum_error_rate=0.02, consecutive_failures=3, failure_threshold=3)
        self.assertEqual(("candidate_is_unhealthy", "error_rate_budget_exceeded", "consecutive_failure_threshold_reached"), reasons)

    def test_invalid_observation_bounds_are_rejected(self):
        with self.assertRaises(ValueError):
            rollback_reasons(healthy=True, error_rate=1.1, maximum_error_rate=0.02, consecutive_failures=0, failure_threshold=3)


if __name__ == "__main__":
    unittest.main()
