import unittest

from compose_zero_downtime.release_metadata import (
    missing_release_metadata,
    release_metadata_is_complete,
    release_metadata_warnings,
)


class ReleaseMetadataTests(unittest.TestCase):
    def test_complete_metadata_passes(self):
        self.assertTrue(
            release_metadata_is_complete(
                {"commit_sha": "abcdef1", "image": "api:v1.0.0", "target_color": "blue", "deploy_actor": "ci"}
            )
        )

    def test_missing_metadata_is_reported(self):
        self.assertIn("image", missing_release_metadata({"commit_sha": "abc"}))

    def test_invalid_color_and_short_sha_are_reported(self):
        warnings = release_metadata_warnings(
            {"commit_sha": "abc", "image": "api:v1.0.0", "target_color": "red", "deploy_actor": "ci"}
        )

        self.assertIn("commit_sha_too_short", warnings)
        self.assertIn("target_color_must_be_blue_or_green", warnings)


if __name__ == "__main__":
    unittest.main()
