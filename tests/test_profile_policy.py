import unittest

from compose_zero_downtime.profile_policy import compose_profiles_are_ready, missing_color_profiles


class ProfilePolicyTests(unittest.TestCase):
    def test_blue_green_profiles_are_ready(self):
        self.assertTrue(compose_profiles_are_ready({"blue", "green"}))

    def test_missing_profile_is_reported(self):
        self.assertEqual(missing_color_profiles({"blue"}), ("green",))


if __name__ == "__main__":
    unittest.main()
