import unittest

from compose_zero_downtime.image_tag_policy import image_tag_is_immutable, image_tag_warnings


class ImageTagPolicyTests(unittest.TestCase):
    def test_versioned_tag_is_accepted(self):
        self.assertTrue(image_tag_is_immutable("registry.example.com/app/api:v1.2.3"))

    def test_latest_tag_is_rejected(self):
        warnings = image_tag_warnings("registry.example.com/app/api:latest")

        self.assertIn("latest_tag_is_not_immutable", warnings)


if __name__ == "__main__":
    unittest.main()
