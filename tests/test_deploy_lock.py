import unittest

from compose_zero_downtime.deploy_lock import deploy_lock_is_valid, deploy_lock_warnings


class DeployLockTests(unittest.TestCase):
    def test_valid_lock_passes(self):
        self.assertTrue(deploy_lock_is_valid({"name": "prod", "owner": "pipeline", "ttl_seconds": 900}))

    def test_missing_lock_fields_are_reported(self):
        warnings = deploy_lock_warnings({"ttl_seconds": 0})

        self.assertIn("lock_name_missing", warnings)
        self.assertIn("ttl_seconds_must_be_positive", warnings)


if __name__ == "__main__":
    unittest.main()
