import unittest

from compose_zero_downtime.health_signal_quorum import health_signal_quorum_is_met, health_signal_quorum_violations


class PromotionHealthSignalQuorumTests(unittest.TestCase):
    def test_two_independent_stable_signals_pass(self):
        signals = [{"probe_id": "http", "status": "passing", "consecutive_successes": 3, "observed_at": "2026-08-23T08:00:00Z"}, {"probe_id": "dependency", "status": "passing", "consecutive_successes": 4, "observed_at": "2026-08-23T08:00:01Z"}]
        self.assertTrue(health_signal_quorum_is_met(signals))

    def test_duplicate_unstable_signal_does_not_form_quorum(self):
        violations = health_signal_quorum_violations([{"probe_id": "http", "status": "failing", "consecutive_successes": 1, "observed_at": "naive"}, {"probe_id": "http", "status": "passing", "consecutive_successes": 3, "observed_at": "2026-08-23T08:00:00Z"}])
        self.assertIn("signal_1:probe_id_must_be_unique", violations)
        self.assertIn("health_signal_quorum_not_met", violations)
