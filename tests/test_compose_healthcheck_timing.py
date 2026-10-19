import unittest
from scripts.validate_compose_healthcheck_timing import compose_healthcheck_timing_violations
class ComposeHealthcheckTimingTests(unittest.TestCase):
    def test_bounded_healthcheck_passes(self):
        check = {'interval_seconds':10, 'timeout_seconds':5, 'retries':6, 'start_period_seconds':30}
        self.assertEqual((), compose_healthcheck_timing_violations([check]))
    def test_invalid_and_unbounded_healthcheck_fails(self):
        check = {'interval_seconds':5, 'timeout_seconds':10, 'retries':100, 'start_period_seconds':0}
        self.assertIn('healthcheck_0:timeout_must_not_exceed_interval', compose_healthcheck_timing_violations([check]))
        self.assertIn('healthcheck_0:worst_case_readiness_exceeds_budget', compose_healthcheck_timing_violations([{'interval_seconds':10,'timeout_seconds':5,'retries':31,'start_period_seconds':0}]))
    def test_invalid_policy_fails(self):
        with self.assertRaises(ValueError): compose_healthcheck_timing_violations([], maximum_readiness_seconds=0)
