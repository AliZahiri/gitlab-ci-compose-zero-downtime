import unittest

from compose_zero_downtime.disk_check import disk_check_passes, disk_check_warnings


class DiskCheckTests(unittest.TestCase):
    def test_enough_disk_passes(self):
        self.assertTrue(disk_check_passes(free_percent=30))

    def test_low_disk_is_reported(self):
        self.assertIn("free_disk_below_deploy_threshold", disk_check_warnings(free_percent=5))


if __name__ == "__main__":
    unittest.main()
