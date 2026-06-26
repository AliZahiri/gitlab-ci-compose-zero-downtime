import unittest

from compose_zero_downtime.image_tag_policy import image_reference_tag, image_tag_is_immutable, image_tag_warnings


class ImageTagPolicyTests(unittest.TestCase):
    def test_versioned_tag_is_accepted(self):
        self.assertTrue(image_tag_is_immutable("registry.example.com/app/api:v1.2.3"))

    def test_latest_tag_is_rejected(self):
        warnings = image_tag_warnings("registry.example.com/app/api:latest")

        self.assertIn("latest_tag_is_not_immutable", warnings)

    def test_non_semver_tag_is_reported(self):
        warnings = image_tag_warnings("registry.example.com/app/api:main")

        self.assertIn("image_tag_should_be_semver", warnings)

    def test_image_reference_tag_ignores_registry_port(self):
        self.assertEqual(image_reference_tag("registry.example.com:5000/app/api:v1.2.3"), "v1.2.3")


if __name__ == "__main__":
    unittest.main()
