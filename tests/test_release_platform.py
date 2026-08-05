import unittest

from compose_zero_downtime.release_platform import release_platform_compatibility_violations, release_platform_is_compatible


class ReleasePlatformCompatibilityGateTests(unittest.TestCase):
    def test_candidate_and_rollback_match_linux_amd64_target(self):
        artifacts = {"candidate": {"image": "registry.example/api@sha256:candidate", "os": "linux", "architecture": "amd64"}, "rollback": {"image": "registry.example/api@sha256:rollback", "os": "Linux", "architecture": "AMD64"}}
        self.assertTrue(release_platform_is_compatible(artifacts, target_os="linux", target_architecture="amd64"))

    def test_missing_image_and_incompatible_platforms_fail(self):
        artifacts = {"candidate": {"image": "", "os": "windows", "architecture": "amd64"}, "rollback": {"image": "registry.example/api@sha256:rollback", "os": "linux", "architecture": "arm64"}}
        violations = release_platform_compatibility_violations(artifacts, target_os="linux", target_architecture="amd64")
        self.assertIn("artifact:candidate:image_is_required", violations)
        self.assertIn("artifact:candidate:os_must_match_target", violations)
        self.assertIn("artifact:rollback:architecture_must_match_target", violations)

    def test_missing_rollback_and_invalid_target_policy_fail(self):
        violations = release_platform_compatibility_violations({"candidate": {"image": "api", "os": "linux", "architecture": "amd64"}}, target_os="linux", target_architecture="amd64")
        self.assertIn("artifact:rollback:platform_evidence_is_required", violations)
        with self.assertRaises(ValueError):
            release_platform_compatibility_violations({}, target_os="linux", target_architecture="")


if __name__ == "__main__":
    unittest.main()
