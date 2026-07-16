import unittest

from compose_zero_downtime.release_health_budget import release_health_is_within_budget, release_health_warnings


class ReleaseHealthBudgetTests(unittest.TestCase):
    def test_clean_probe_summary_passes(self):
        self.assertTrue(release_health_is_within_budget({"successes": 3, "failures": 0}))

    def test_failure_budget_is_enforced(self):
        warnings = release_health_warnings({"successes": 3, "failures": 1})

        self.assertIn("failed_probes_exceed_budget", warnings)


if __name__ == "__main__":
    unittest.main()
