import unittest

from compose_zero_downtime.deploy_lock import deploy_lock_is_valid, deploy_lock_warnings


class DeployLockTests(unittest.TestCase):
    def test_valid_lock_passes(self):
        self.assertTrue(deploy_lock_is_valid({"name": "prod", "owner": "pipeline", "ttl_seconds": 900, "release_on_failure": True}))

    def test_missing_lock_fields_are_reported(self):
        warnings = deploy_lock_warnings({"ttl_seconds": 0})

        self.assertIn("lock_name_missing", warnings)
        self.assertIn("ttl_seconds_must_be_positive", warnings)

    def test_lock_recovery_window_is_bounded(self):
        warnings = deploy_lock_warnings({"name": "prod", "owner": "pipeline", "ttl_seconds": 7200, "release_on_failure": False})

        self.assertIn("ttl_seconds_exceeds_recovery_window", warnings)
        self.assertIn("release_on_failure_must_be_enabled", warnings)


if __name__ == "__main__":
    unittest.main()
