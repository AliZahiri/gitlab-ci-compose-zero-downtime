import unittest

from compose_zero_downtime.smoke_manifest import smoke_manifest_is_ready, smoke_manifest_warnings


class SmokeManifestTests(unittest.TestCase):
    def test_named_smoke_check_passes(self):
        checks = [{"name": "health", "path": "/health", "timeout_seconds": 5}]

        self.assertTrue(smoke_manifest_is_ready(checks))

    def test_missing_timeout_is_reported(self):
        warnings = smoke_manifest_warnings([{"name": "health", "path": "/health"}])

        self.assertIn("check_0_timeout_must_be_positive", warnings)


if __name__ == "__main__":
    unittest.main()
