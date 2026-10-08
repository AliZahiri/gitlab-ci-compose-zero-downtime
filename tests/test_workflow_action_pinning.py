import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"
CHECKOUT = "actions/checkout@d23441a48e516b6c34aea4fa41551a30e30af803"
SETUP_PYTHON = "actions/setup-python@ece7cb06caefa5fff74198d8649806c4678c61a1"


class WorkflowActionPinningTests(unittest.TestCase):
    def test_first_party_actions_are_pinned_by_commit_sha(self):
        content = "\n".join(path.read_text(encoding="utf-8") for path in WORKFLOWS.glob("*.yml"))

        self.assertIn(CHECKOUT, content)
        self.assertIn(SETUP_PYTHON, content)
        self.assertNotIn("actions/checkout@v6", content)
        self.assertNotIn("actions/setup-python@v6", content)


if __name__ == "__main__":
    unittest.main()
