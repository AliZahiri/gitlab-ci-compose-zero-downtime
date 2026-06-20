import unittest

from compose_zero_downtime.health_contract import (
    REQUIRED_READINESS_CHECKS,
    missing_readiness_checks,
    readiness_contract_is_satisfied,
)


class HealthContractTests(unittest.TestCase):
    def test_complete_contract_is_satisfied(self):
        self.assertTrue(readiness_contract_is_satisfied(REQUIRED_READINESS_CHECKS))

    def test_missing_checks_are_reported(self):
        missing = missing_readiness_checks({"http_accepting_requests"})

        self.assertIn("critical_dependencies_reachable", missing)
        self.assertIn("minimal_real_request_served", missing)


if __name__ == "__main__":
    unittest.main()
