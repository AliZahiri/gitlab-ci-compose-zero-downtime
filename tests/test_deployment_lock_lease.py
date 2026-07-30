import unittest
from datetime import datetime, timezone

from compose_zero_downtime.deployment_lock_lease import deployment_lock_lease_is_usable, deployment_lock_lease_violations


NOW = datetime(2026, 7, 30, 8, 0, tzinfo=timezone.utc)


class DeploymentLockLeaseContractTests(unittest.TestCase):
    def test_owned_bounded_lease_with_sufficient_time_passes(self):
        lease = {"lease_id": "deploy:orders:42", "holder": "runner-12", "acquired_at": "2026-07-30T07:55:00Z", "expires_at": "2026-07-30T08:15:00Z"}
        self.assertTrue(deployment_lock_lease_is_usable(lease, now=NOW))

    def test_expired_oversized_and_unowned_lease_fail(self):
        lease = {"lease_id": "bad", "holder": "", "acquired_at": "2026-07-30T06:00:00Z", "expires_at": "2026-07-30T07:00:00Z"}
        violations = deployment_lock_lease_violations(lease, now=NOW)
        self.assertIn("lease_id_is_invalid", violations)
        self.assertIn("lease_holder_is_required", violations)
        self.assertIn("lease_duration_exceeds_maximum", violations)
        self.assertIn("lease_remaining_time_is_insufficient", violations)

    def test_naive_timestamps_and_invalid_policy_fail(self):
        violations = deployment_lock_lease_violations({"lease_id": "deploy:valid", "holder": "runner", "acquired_at": "2026-07-30T07:00:00", "expires_at": "2026-07-30T08:10:00"}, now=NOW)
        self.assertIn("acquired_at_must_be_timezone_aware", violations)
        self.assertIn("expires_at_must_be_timezone_aware", violations)
        with self.assertRaises(ValueError):
            deployment_lock_lease_violations({}, now=NOW, maximum_duration_seconds=30, minimum_remaining_seconds=60)


if __name__ == "__main__":
    unittest.main()
