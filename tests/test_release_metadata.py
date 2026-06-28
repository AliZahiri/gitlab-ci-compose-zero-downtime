import unittest

from compose_zero_downtime.release_metadata import missing_release_metadata, release_metadata_is_complete


class ReleaseMetadataTests(unittest.TestCase):
    def test_complete_metadata_passes(self):
        self.assertTrue(release_metadata_is_complete({"commit_sha": "abc", "image": "api:v1.0.0", "target_color": "blue", "deploy_actor": "ci"}))

    def test_missing_metadata_is_reported(self):
        self.assertIn("image", missing_release_metadata({"commit_sha": "abc"}))


if __name__ == "__main__":
    unittest.main()
