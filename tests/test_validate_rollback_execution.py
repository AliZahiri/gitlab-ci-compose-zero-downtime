import unittest
from datetime import datetime, timezone
from scripts.validate_rollback_execution import rollback_execution_violations
NOW=datetime(2026,9,13,12,tzinfo=timezone.utc)
class RollbackExecutionTests(unittest.TestCase):
    def test_fresh_successful_rollback_passes(self):
        e={'failed_release':'green-2','restored_release':'blue-1','rollback_succeeded':True,'post_rollback_smoke_passed':True,'observed_at':'2026-09-13T11:55:00Z'}
        self.assertEqual((),rollback_execution_violations(e,failed_release='green-2',stable_release='blue-1',now=NOW))
    def test_wrong_failed_and_stale_rollback_fails(self):
        e={'failed_release':'other','restored_release':'other','rollback_succeeded':False,'post_rollback_smoke_passed':False,'observed_at':'2026-09-12T00:00:00Z'}
        v=rollback_execution_violations(e,failed_release='green-2',stable_release='blue-1',now=NOW)
        self.assertIn('rollback_must_succeed',v); self.assertIn('post_rollback_smoke_test_must_pass',v); self.assertIn('rollback_evidence_is_invalid_stale_or_future_dated',v)
    def test_invalid_policy_fails(self):
        with self.assertRaises(ValueError): rollback_execution_violations({},failed_release='same',stable_release='same',now=NOW)
