import unittest
from pathlib import Path


WORKFLOW_PATH = Path(__file__).resolve().parents[1] / ".github/workflows/daily-pr.yml"
EXPECTED_CRON = 'cron: "25 4 * * *"'
EXPECTED_EMAIL = "1667664+AliZahiri@users.noreply.github.com"


class DailyWorkflowPolicyTests(unittest.TestCase):
    def test_daily_run_uses_the_portfolio_maintenance_window(self):
        workflow = WORKFLOW_PATH.read_text(encoding="utf-8")

        self.assertIn("# 07:55 Asia/Tehran (UTC+03:30)", workflow)
        self.assertEqual(1, workflow.count("cron:"))
        self.assertIn(EXPECTED_CRON, workflow)

    def test_automation_commits_use_the_declared_portfolio_identity(self):
        workflow = WORKFLOW_PATH.read_text(encoding="utf-8")

        self.assertIn(EXPECTED_EMAIL, workflow)


if __name__ == "__main__":
    unittest.main()
