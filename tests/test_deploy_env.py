import unittest

from compose_zero_downtime.deploy_env import REQUIRED_DEPLOY_ENV_VARS, deploy_env_is_complete, missing_deploy_env_vars


class DeployEnvTests(unittest.TestCase):
    def test_complete_env_passes(self):
        self.assertTrue(deploy_env_is_complete({name: "value" for name in REQUIRED_DEPLOY_ENV_VARS}))

    def test_missing_env_vars_are_reported(self):
        missing = missing_deploy_env_vars({"DEPLOY_HOST": "example.com"})

        self.assertIn("APP_IMAGE", missing)
        self.assertIn("DEPLOY_PATH", missing)


if __name__ == "__main__":
    unittest.main()
