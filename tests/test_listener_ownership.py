import unittest
from datetime import datetime, timezone

from compose_zero_downtime.listener_ownership import candidate_listeners_are_owned, listener_ownership_violations


NOW = datetime(2026, 8, 28, 12, 0, tzinfo=timezone.utc)


class CandidateListenerOwnershipEvidenceTests(unittest.TestCase):
    def test_fresh_distinct_owned_blue_green_listeners_pass(self):
        listeners = [{"color": "blue", "host": "127.0.0.1", "port": 8081, "project_name": "payments-prod", "container_id": "a" * 12, "listening": True, "observed_at": "2026-08-28T11:59:00Z"}, {"color": "green", "host": "127.0.0.1", "port": 8082, "project_name": "payments-prod", "container_id": "b" * 12, "listening": True, "observed_at": "2026-08-28T11:59:30Z"}]
        self.assertTrue(candidate_listeners_are_owned(listeners, expected_project="payments-prod", now=NOW))

    def test_duplicate_endpoint_wrong_owner_and_stale_listener_fail(self):
        listener = {"color": "blue", "host": "127.0.0.1", "port": 8081, "project_name": "other", "container_id": "bad", "listening": False, "observed_at": "2026-08-28T10:00:00Z"}
        violations = listener_ownership_violations([listener, {**listener, "color": "green"}], expected_project="payments-prod", now=NOW)
        self.assertIn("listener_1:endpoint_must_be_unique", violations)
        self.assertIn("listener_0:project_owner_does_not_match", violations)
        self.assertIn("listener_0:observation_is_stale_or_invalid", violations)

    def test_missing_color_and_invalid_policy_fail(self):
        listener = {"color": "blue", "host": "127.0.0.1", "port": 8081, "project_name": "api-prod", "container_id": "a" * 12, "listening": True, "observed_at": "2026-08-28T12:00:00Z"}
        self.assertIn("green_listener_is_required", listener_ownership_violations([listener], expected_project="api-prod", now=NOW))
        with self.assertRaises(ValueError):
            listener_ownership_violations([], expected_project="", now=NOW)
