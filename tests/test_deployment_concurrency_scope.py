import unittest
from datetime import datetime, timezone

from compose_zero_downtime.deployment_concurrency_scope import deployment_concurrency_scope_is_safe, deployment_concurrency_scope_violations


NOW = datetime(2026, 8, 13, 6, 0, tzinfo=timezone.utc)


class DeploymentConcurrencyScopeGateTests(unittest.TestCase):
    def test_unique_bounded_lease_passes(self):
        leases = [{"lease_id": "release-1", "environment": "production", "traffic_target": "api", "expires_at": "2026-08-13T06:10:00Z"}]
        self.assertTrue(deployment_concurrency_scope_is_safe(leases, now=NOW))

    def test_duplicate_and_expired_scope_fail(self):
        leases = [{"lease_id": "release-1", "environment": "production", "traffic_target": "api", "expires_at": "2026-08-13T05:00:00Z"}, {"lease_id": "release-1", "environment": "production", "traffic_target": "api", "expires_at": "2026-08-13T06:10:00Z"}]
        violations = deployment_concurrency_scope_violations(leases, now=NOW)
        self.assertIn("lease_0:expiry_must_be_within_lease_budget", violations)
        self.assertIn("lease_1:lease_id_must_be_unique", violations)
        self.assertIn("lease_1:environment_must_be_unique", violations)
        self.assertIn("lease_1:traffic_target_must_be_unique", violations)


if __name__ == "__main__":
    unittest.main()
