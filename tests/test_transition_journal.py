import unittest

from compose_zero_downtime.transition_journal import transition_journal_is_valid, transition_journal_violations


class TransitionJournalTests(unittest.TestCase):
    def test_complete_promotion_and_explicit_rollback_are_valid(self):
        self.assertTrue(transition_journal_is_valid(["prepared", "candidate_started", "candidate_healthy", "proxy_validated", "promoted"]))
        self.assertTrue(transition_journal_is_valid(["prepared", "candidate_started", "rolled_back"]))

    def test_skipped_and_duplicate_states_fail(self):
        self.assertEqual(("deployment_transition_order_is_invalid",), transition_journal_violations(["prepared", "candidate_healthy"]))
        self.assertEqual(("deployment_transition_states_must_be_unique",), transition_journal_violations(["prepared", "prepared"]))


if __name__ == "__main__":
    unittest.main()
