#!/usr/bin/env python3
"""Validate fresh rollback execution evidence against approved releases."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path


def _timestamp(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        return None
    return parsed


def _validate_policy(
    *,
    failed_release: object,
    stable_release: object,
    now: object,
    maximum_age_seconds: object,
) -> None:
    for label, release in (
        ("failed_release", failed_release),
        ("stable_release", stable_release),
    ):
        if not isinstance(release, str) or not release or release != release.strip():
            raise ValueError(f"{label} must be a nonempty, trimmed string")
    if failed_release == stable_release:
        raise ValueError("failed_release and stable_release must differ")
    if not isinstance(now, datetime) or now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("now must be timezone-aware")
    if type(maximum_age_seconds) is not int or maximum_age_seconds < 1:
        raise ValueError("maximum_age_seconds must be a positive integer")


def rollback_execution_violations(
    evidence: object,
    *,
    failed_release: str,
    stable_release: str,
    now: datetime,
    maximum_age_seconds: int = 900,
) -> tuple[str, ...]:
    """Return deterministic policy violations for one rollback observation."""
    _validate_policy(
        failed_release=failed_release,
        stable_release=stable_release,
        now=now,
        maximum_age_seconds=maximum_age_seconds,
    )
    if not isinstance(evidence, dict):
        return ("rollback_evidence_must_be_an_object",)

    violations: list[str] = []
    if evidence.get("failed_release") != failed_release:
        violations.append("failed_release_must_match_approved_release")
    if evidence.get("restored_release") != stable_release:
        violations.append("restored_release_must_match_last_stable_release")
    if evidence.get("rollback_succeeded") is not True:
        violations.append("rollback_must_succeed")
    if evidence.get("post_rollback_smoke_passed") is not True:
        violations.append("post_rollback_smoke_test_must_pass")

    observed_at = _timestamp(evidence.get("observed_at"))
    if (
        observed_at is None
        or not 0 <= (now - observed_at).total_seconds() <= maximum_age_seconds
    ):
        violations.append("rollback_evidence_is_invalid_stale_or_future_dated")
    return tuple(violations)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path, help="Rollback evidence manifest")
    parser.add_argument("--now", required=True, help="Timezone-aware ISO 8601 decision time")
    parser.add_argument("--maximum-age-seconds", type=int, default=900)
    args = parser.parse_args(argv)

    try:
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
        if not isinstance(manifest, dict):
            raise ValueError("manifest must be an object")
        expected = manifest.get("expected")
        if not isinstance(expected, dict) or set(expected) != {
            "failed_release",
            "stable_release",
        }:
            raise ValueError("expected must contain exactly the approved releases")
        now = _timestamp(args.now)
        if now is None:
            raise ValueError("--now must be timezone-aware")
        violations = rollback_execution_violations(
            manifest.get("evidence"),
            failed_release=expected["failed_release"],
            stable_release=expected["stable_release"],
            now=now,
            maximum_age_seconds=args.maximum_age_seconds,
        )
    except (OSError, UnicodeError, ValueError):
        print(
            json.dumps(
                {"error": "invalid_manifest_or_policy", "status": "error"},
                sort_keys=True,
            )
        )
        return 2

    status = "rejected" if violations else "passed"
    print(json.dumps({"status": status, "violations": list(violations)}, sort_keys=True))
    return 1 if violations else 0


if __name__ == "__main__":
    raise SystemExit(main())
