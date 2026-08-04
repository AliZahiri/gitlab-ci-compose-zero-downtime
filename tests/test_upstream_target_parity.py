import unittest

from compose_zero_downtime.upstream_target_parity import nginx_upstreams_match_plan, upstream_target_parity_violations


class NginxUpstreamTargetParityGateTests(unittest.TestCase):
    def test_valid_rendered_candidate_targets_match_plan(self):
        self.assertTrue(nginx_upstreams_match_plan(expected_targets=("app-green-1:8080", "app-green-2:8080"), rendered_targets=["app-green-2:8080", "app-green-1:8080"], nginx_config_valid=True))

    def test_invalid_config_duplicate_missing_and_old_target_fail(self):
        violations = upstream_target_parity_violations(expected_targets=("app-green:8080",), rendered_targets=["app-blue:8080", "app-blue:8080"], nginx_config_valid=False)
        self.assertIn("nginx_configuration_must_be_valid", violations)
        self.assertIn("rendered_targets_must_be_unique", violations)
        self.assertIn("expected_upstream_target_is_missing", violations)
        self.assertIn("unexpected_upstream_target_is_rendered", violations)

    def test_invalid_expected_plan_fails(self):
        with self.assertRaises(ValueError):
            upstream_target_parity_violations(expected_targets=("app:8080", "app:8080"), rendered_targets=[], nginx_config_valid=True)


if __name__ == "__main__":
    unittest.main()
