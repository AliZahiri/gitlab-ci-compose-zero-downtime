import unittest

from compose_zero_downtime.smoke_plan import (
    REQUIRED_SMOKE_CHECKS,
    missing_smoke_checks,
    smoke_plan_is_complete,
    smoke_plan_warnings,
)


class SmokePlanTests(unittest.TestCase):
    def test_complete_smoke_plan_passes(self):
        self.assertTrue(smoke_plan_is_complete(REQUIRED_SMOKE_CHECKS))

    def test_missing_smoke_checks_are_reported(self):
        missing = missing_smoke_checks({"public_endpoint_success"})

        self.assertIn("critical_api_route", missing)
        self.assertIn("stable_error_rate", missing)

    def test_smoke_timeout_must_fit_release_budget(self):
        warnings = smoke_plan_warnings(REQUIRED_SMOKE_CHECKS, timeout_seconds=30.0)

        self.assertIn("timeout_seconds_exceeds_release_budget", warnings)
        self.assertFalse(smoke_plan_is_complete(REQUIRED_SMOKE_CHECKS, timeout_seconds=30.0))


if __name__ == "__main__":
    unittest.main()
