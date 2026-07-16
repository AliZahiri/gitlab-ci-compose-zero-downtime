import unittest

from compose_zero_downtime.environment_contract import environment_contract_is_ready, missing_environment_keys


class EnvironmentContractTests(unittest.TestCase):
    def test_complete_environment_passes(self):
        self.assertTrue(environment_contract_is_ready({"IMAGE_TAG": "sha", "APP_PORT": "8080"}, ("IMAGE_TAG", "APP_PORT")))

    def test_missing_environment_is_reported(self):
        self.assertEqual(("APP_PORT",), missing_environment_keys({"IMAGE_TAG": "sha"}, ("IMAGE_TAG", "APP_PORT")))


if __name__ == "__main__":
    unittest.main()
