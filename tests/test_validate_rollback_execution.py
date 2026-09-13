import json
import tempfile
import unittest
from contextlib import redirect_stdout
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path

from scripts.validate_rollback_execution import main, rollback_execution_violations


NOW = datetime(2026, 9, 13, 12, tzinfo=timezone.utc)
FAILED_RELEASE = "orders-20260913.2"
STABLE_RELEASE = "orders-20260913.1"


def valid_evidence() -> dict[str, object]:
    return {
        "failed_release": FAILED_RELEASE,
        "restored_release": STABLE_RELEASE,
        "rollback_succeeded": True,
        "post_rollback_smoke_passed": True,
        "observed_at": "2026-09-13T11:55:00Z",
    }


class RollbackExecutionTests(unittest.TestCase):
    def test_fresh_successful_rollback_passes(self):
        self.assertEqual(
            (),
            rollback_execution_violations(
                valid_evidence(),
                failed_release=FAILED_RELEASE,
                stable_release=STABLE_RELEASE,
                now=NOW,
            ),
        )

    def test_evidence_must_bind_both_approved_releases(self):
        cases = (
            ("failed_release", "other", "failed_release_must_match_approved_release"),
            (
                "restored_release",
                "other",
                "restored_release_must_match_last_stable_release",
            ),
        )
        for field, value, violation in cases:
            with self.subTest(field=field):
                evidence = {**valid_evidence(), field: value}
                self.assertIn(
                    violation,
                    rollback_execution_violations(
                        evidence,
                        failed_release=FAILED_RELEASE,
                        stable_release=STABLE_RELEASE,
                        now=NOW,
                    ),
                )

    def test_success_and_smoke_results_must_be_literal_true(self):
        for field, violation in (
            ("rollback_succeeded", "rollback_must_succeed"),
            ("post_rollback_smoke_passed", "post_rollback_smoke_test_must_pass"),
        ):
            for value in (None, False, 1, "true", [], {}):
                with self.subTest(field=field, value=value):
                    evidence = {**valid_evidence(), field: value}
                    self.assertIn(
                        violation,
                        rollback_execution_violations(
                            evidence,
                            failed_release=FAILED_RELEASE,
                            stable_release=STABLE_RELEASE,
                            now=NOW,
                        ),
                    )

    def test_invalid_stale_and_future_observations_fail(self):
        for observed_at in (
            None,
            True,
            "invalid",
            "2026-09-13T11:45:00",
            "2026-09-13T11:44:59Z",
            "2026-09-13T12:00:01Z",
        ):
            with self.subTest(observed_at=observed_at):
                evidence = {**valid_evidence(), "observed_at": observed_at}
                self.assertIn(
                    "rollback_evidence_is_invalid_stale_or_future_dated",
                    rollback_execution_violations(
                        evidence,
                        failed_release=FAILED_RELEASE,
                        stable_release=STABLE_RELEASE,
                        now=NOW,
                    ),
                )

    def test_age_boundaries_and_equivalent_timezone_pass(self):
        for observed_at in (
            "2026-09-13T11:45:00Z",
            "2026-09-13T12:00:00Z",
            "2026-09-13T15:25:00+03:30",
        ):
            with self.subTest(observed_at=observed_at):
                evidence = {**valid_evidence(), "observed_at": observed_at}
                self.assertEqual(
                    (),
                    rollback_execution_violations(
                        evidence,
                        failed_release=FAILED_RELEASE,
                        stable_release=STABLE_RELEASE,
                        now=NOW,
                    ),
                )

    def test_invalid_policy_fails_closed(self):
        for maximum_age_seconds in (0, -1, True, 1.5):
            with self.subTest(maximum_age_seconds=maximum_age_seconds):
                with self.assertRaises(ValueError):
                    rollback_execution_violations(
                        valid_evidence(),
                        failed_release=FAILED_RELEASE,
                        stable_release=STABLE_RELEASE,
                        now=NOW,
                        maximum_age_seconds=maximum_age_seconds,
                    )
        for failed_release, stable_release in (
            ("", STABLE_RELEASE),
            (" padded ", STABLE_RELEASE),
            (FAILED_RELEASE, ""),
            (FAILED_RELEASE, FAILED_RELEASE),
        ):
            with self.subTest(
                failed_release=failed_release,
                stable_release=stable_release,
            ):
                with self.assertRaises(ValueError):
                    rollback_execution_violations(
                        valid_evidence(),
                        failed_release=failed_release,
                        stable_release=stable_release,
                        now=NOW,
                    )
        with self.assertRaises(ValueError):
            rollback_execution_violations(
                valid_evidence(),
                failed_release=FAILED_RELEASE,
                stable_release=STABLE_RELEASE,
                now=NOW.replace(tzinfo=None),
            )

    def test_invalid_evidence_shape_is_rejected(self):
        self.assertEqual(
            ("rollback_evidence_must_be_an_object",),
            rollback_execution_violations(
                [],
                failed_release=FAILED_RELEASE,
                stable_release=STABLE_RELEASE,
                now=NOW,
            ),
        )

    def test_cli_exit_codes_distinguish_rejection_and_input_error(self):
        expected = {
            "failed_release": FAILED_RELEASE,
            "stable_release": STABLE_RELEASE,
        }
        with tempfile.TemporaryDirectory() as directory:
            manifest = Path(directory) / "rollback.json"
            cases = (
                ({"expected": expected, "evidence": valid_evidence()}, 0, "passed"),
                ({"expected": expected, "evidence": {}}, 1, "rejected"),
                (
                    {"expected": {"failed_release": FAILED_RELEASE}, "evidence": {}},
                    2,
                    "error",
                ),
                ([], 2, "error"),
            )
            for payload, exit_code, status in cases:
                with self.subTest(status=status, exit_code=exit_code):
                    manifest.write_text(json.dumps(payload), encoding="utf-8")
                    stdout = StringIO()
                    with redirect_stdout(stdout):
                        result = main([str(manifest), "--now", NOW.isoformat()])
                    self.assertEqual(exit_code, result)
                    self.assertEqual(status, json.loads(stdout.getvalue())["status"])

            manifest.write_text("{invalid", encoding="utf-8")
            with redirect_stdout(StringIO()):
                self.assertEqual(2, main([str(manifest), "--now", NOW.isoformat()]))
            with redirect_stdout(StringIO()):
                self.assertEqual(
                    2,
                    main([str(manifest.parent / "missing.json"), "--now", NOW.isoformat()]),
                )


if __name__ == "__main__":
    unittest.main()
