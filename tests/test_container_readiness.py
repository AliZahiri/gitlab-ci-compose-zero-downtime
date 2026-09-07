import json
import os
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

from compose_zero_downtime import cli


class ContainerReadinessTests(unittest.TestCase):
    def test_documented_entry_points_execute_dry_run(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            template = root / "deploy/nginx/default.conf.tpl"
            template.parent.mkdir(parents=True)
            template.write_text("server app_{{ACTIVE_COLOR}}:{{APP_PORT}};", encoding="utf-8")
            repo = Path(cli.__file__).resolve().parents[1]
            options = ["green", "--root", str(root), "--dry-run", "--plan-json"]
            commands = [
                [sys.executable, "-m", "compose_zero_downtime", "deploy", *options],
                ["bash", str(repo / "deploy/blue-green-deploy.sh"), *options],
            ]
            for command in commands:
                with self.subTest(command=command):
                    result = subprocess.run(command, cwd=repo, capture_output=True, text=True, timeout=10)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual(json.loads(result.stdout)["target_color"], "green")
                    self.assertFalse((root / "deploy/nginx/default.conf").exists())
                    self.assertFalse((root / "deploy" / ".active-color").exists())

    def test_health_requires_running_lifecycle_state(self):
        cases = [
            ({"Status": "running"}, "running"),
            ({"Status": "running", "Health": {"Status": "healthy"}}, "healthy"),
            ({"Status": "running", "Health": {"Status": "starting"}}, "starting"),
            ({"Status": "running", "Health": {"Status": "unhealthy"}}, "unhealthy"),
            ({"Status": "exited"}, "exited"),
            ({"Status": "created"}, "created"),
            ({"Status": "dead"}, "dead"),
            ({"Status": "removing"}, "removing"),
        ]
        cases.extend(
            ({"Status": status, "Health": {"Status": "healthy"}}, status)
            for status in ("exited", "paused", "restarting", "dead", "removing")
        )
        for state, expected in cases:
            with self.subTest(state=state), mock.patch.object(cli, "run") as run:
                run.return_value = subprocess.CompletedProcess([], 0, json.dumps(state))
                self.assertEqual(cli.container_health("candidate"), expected)

    def test_invalid_inspect_json_cannot_report_readiness(self):
        with mock.patch.object(cli, "run") as run:
            run.return_value = subprocess.CompletedProcess([], 0, "not JSON")
            with self.assertRaises(ValueError):
                cli.container_health("candidate")

    def test_inspect_failure_is_propagated(self):
        with mock.patch.object(cli, "run", side_effect=subprocess.CalledProcessError(1, ["docker"])):
            with self.assertRaises(subprocess.CalledProcessError):
                cli.wait_for_ready("candidate", "backend", 2, 0)

    def test_terminal_states_fail_without_waiting_for_timeout(self):
        for status in ("exited", "dead", "removing", "unhealthy"):
            with (
                self.subTest(status=status),
                mock.patch.object(cli, "container_health", return_value=status),
                mock.patch.object(cli, "run"),
                mock.patch.object(cli.time, "sleep") as sleep,
            ):
                with self.assertRaisesRegex(RuntimeError, status):
                    cli.wait_for_ready("candidate", "backend", 3, 1)
                sleep.assert_not_called()

    def test_starting_and_restarting_wait_until_healthy(self):
        with (
            mock.patch.object(cli, "container_health", side_effect=["restarting", "starting", "healthy"]) as health,
            mock.patch.object(cli.time, "sleep"),
        ):
            cli.wait_for_ready("candidate", "backend", 3, 0)
            self.assertEqual(health.call_count, 3)

    def test_running_without_healthcheck_preserves_compatibility(self):
        with mock.patch.object(cli, "run") as run:
            run.return_value = subprocess.CompletedProcess([], 0, json.dumps({"Status": "running"}))
            cli.wait_for_ready("candidate", "backend", 1, 0)

    def test_nonready_states_exhaust_the_attempt_budget(self):
        for status in ("starting", "created", "paused", "restarting"):
            with (
                self.subTest(status=status),
                mock.patch.object(cli, "container_health", return_value=status) as health,
                mock.patch.object(cli.time, "sleep"),
            ):
                with self.assertRaises(TimeoutError):
                    cli.wait_for_ready("candidate", "backend", 2, 0)
                self.assertEqual(health.call_count, 2)

    def test_exited_candidate_preserves_active_traffic_configuration(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            template = root / "deploy/nginx/default.conf.tpl"
            template.parent.mkdir(parents=True)
            template.write_text("server app_{{ACTIVE_COLOR}}:{{APP_PORT}};", encoding="utf-8")
            config = root / "deploy/nginx/default.conf"
            config.write_text("previous configuration", encoding="utf-8")
            active = root / "deploy" / ".active-color"
            active.write_text("blue\n", encoding="utf-8")

            def run(command, **kwargs):
                output = json.dumps({"Status": "exited"}) if command[:2] == ["docker", "inspect"] else ""
                return subprocess.CompletedProcess(command, 0, output)

            with (
                mock.patch.dict(os.environ, {}, clear=True),
                mock.patch.object(cli, "run", side_effect=run) as commands,
                mock.patch.object(cli, "get_container_id", return_value="candidate"),
                mock.patch.object(cli.time, "sleep"),
                redirect_stdout(StringIO()),
            ):
                args = cli.build_parser().parse_args([
                    "deploy", "green", "--root", str(root),
                    "--health-attempts", "1", "--health-interval", "0",
                ])
                with self.assertRaisesRegex(RuntimeError, "exited"):
                    args.func(args)

            self.assertEqual(config.read_text(encoding="utf-8"), "previous configuration")
            self.assertEqual(active.read_text(encoding="utf-8"), "blue\n")
            compose_calls = [
                call.args[0] for call in commands.call_args_list
                if call.args[0][:2] == ["docker", "compose"]
            ]
            self.assertEqual(len(compose_calls), 1)
            self.assertEqual(compose_calls[0][-3:-1], ["up", "-d"])


if __name__ == "__main__":
    unittest.main()
