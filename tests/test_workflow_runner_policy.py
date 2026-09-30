import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"
RUNS_ON = re.compile(r"^\s*runs-on:\s*([^\s#]+)", re.MULTILINE)
EXPECTED_RUNNER = "ubuntu-26.04"


class WorkflowRunnerPolicyTests(unittest.TestCase):
    def test_all_jobs_use_the_validated_ubuntu_runner(self) -> None:
        runners: list[tuple[Path, str]] = []

        for workflow in sorted(WORKFLOWS.glob("*.yml")):
            content = workflow.read_text(encoding="utf-8")
            runners.extend((workflow, runner) for runner in RUNS_ON.findall(content))

        self.assertTrue(runners, "expected at least one workflow runner")
        for workflow, runner in runners:
            with self.subTest(workflow=workflow.name):
                self.assertEqual(EXPECTED_RUNNER, runner)


if __name__ == "__main__":
    unittest.main()
