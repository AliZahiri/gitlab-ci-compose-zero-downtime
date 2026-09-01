import unittest

from compose_zero_downtime.volume_write_isolation import volume_write_isolation_violations, volumes_are_write_isolated


class BlueGreenVolumeWriteIsolationTests(unittest.TestCase):
    def test_distinct_data_and_shared_read_only_config_pass(self):
        active = [{"source": "blue-data", "target": "/data", "read_only": False}, {"source": "trust-bundle", "target": "/trust", "read_only": True}]
        candidate = [{"source": "green-data", "target": "/data", "read_only": False}, {"source": "trust-bundle", "target": "/trust", "read_only": True}]
        self.assertTrue(volumes_are_write_isolated(active, candidate))

    def test_shared_writable_source_fails(self):
        active = [{"source": "app-data", "target": "/data", "read_only": False}]
        candidate = [{"source": "app-data", "target": "/data", "read_only": True}]
        self.assertIn("shared_writable_volume:app-data", volume_write_isolation_violations(active, candidate))

    def test_duplicate_and_relative_targets_fail(self):
        mounts = [{"source": "one", "target": "data", "read_only": False}, {"source": "two", "target": "/data", "read_only": False}, {"source": "three", "target": "/data", "read_only": False}]
        violations = volume_write_isolation_violations(mounts, [])
        self.assertIn("active:mount_0_target_must_be_absolute", violations)
        self.assertIn("active:mount_targets_must_be_unique", violations)
