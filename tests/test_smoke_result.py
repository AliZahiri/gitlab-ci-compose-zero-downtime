import unittest

from compose_zero_downtime.smoke_result import smoke_result_passed, summarize_smoke_result


class SmokeResultTests(unittest.TestCase):
    def test_fast_success_passes(self):
        result = {"name": "health", "target": "https://example.com/health", "status_code": 200, "duration_ms": 120}

        self.assertTrue(smoke_result_passed(result))
        self.assertTrue(summarize_smoke_result(result)["passed"])

    def test_slow_or_error_result_fails(self):
        self.assertFalse(smoke_result_passed({"status_code": 503, "duration_ms": 100}))
        self.assertFalse(smoke_result_passed({"status_code": 200, "duration_ms": 5000}))


if __name__ == "__main__":
    unittest.main()
