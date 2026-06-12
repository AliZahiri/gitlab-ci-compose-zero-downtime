import tempfile
import unittest
from pathlib import Path

from compose_zero_downtime.cli import (
    build_smoke_url,
    choose_next_color,
    read_active_color,
    render_nginx_config,
)


class ComposeZeroDowntimeTests(unittest.TestCase):
    def test_choose_next_color_toggles_without_request(self):
        self.assertEqual(choose_next_color("blue"), "green")
        self.assertEqual(choose_next_color("green"), "blue")

    def test_choose_next_color_validates_requested_color(self):
        self.assertEqual(choose_next_color("blue", "blue"), "blue")
        with self.assertRaises(ValueError):
            choose_next_color("blue", "red")

    def test_read_active_color_defaults_to_blue(self):
        missing = Path(tempfile.gettempdir()) / "missing-active-color"
        self.assertEqual(read_active_color(missing), "blue")

    def test_render_nginx_config_replaces_placeholders(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            template = tmp / "default.conf.tpl"
            output = tmp / "default.conf"
            template.write_text("server app_{{ACTIVE_COLOR}}:{{APP_PORT}};", encoding="utf-8")

            render_nginx_config(template, output, "green", "8080")

            self.assertEqual(output.read_text(encoding="utf-8"), "server app_green:8080;")

    def test_build_smoke_url_joins_base_and_path(self):
        self.assertEqual(
            build_smoke_url("https://example.com/app/", "/health"),
            "https://example.com/app/health",
        )


if __name__ == "__main__":
    unittest.main()
