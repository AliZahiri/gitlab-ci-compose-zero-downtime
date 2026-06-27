import unittest

from compose_zero_downtime.nginx_validation import nginx_validation_plan_is_safe, nginx_validation_warnings


class NginxValidationTests(unittest.TestCase):
    def test_safe_plan_passes(self):
        plan = {"rendered_config_path": "deploy/nginx/default.conf", "validation_required": True, "reload_on_validation_failure": False}

        self.assertTrue(nginx_validation_plan_is_safe(plan))

    def test_reload_after_failed_validation_is_reported(self):
        warnings = nginx_validation_warnings({"validation_required": False, "reload_on_validation_failure": True})

        self.assertIn("validation_must_be_required", warnings)
        self.assertIn("must_not_reload_on_validation_failure", warnings)


if __name__ == "__main__":
    unittest.main()
