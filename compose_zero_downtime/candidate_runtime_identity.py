from __future__ import annotations

from datetime import datetime
import re

_DIGEST = re.compile(r"sha256:[0-9a-f]{64}\Z")
_FINGERPRINT = re.compile(r"[0-9a-f]{64}\Z")


def candidate_runtime_identity_violations(expected: dict[str, object], observed: dict[str, object]) -> tuple[str, ...]:
    violations: list[str] = []
    digest = expected.get("image_digest")
    if not isinstance(digest, str) or not _DIGEST.fullmatch(digest):
        violations.append("expected_image_digest_must_be_immutable")
    elif observed.get("image_digest") != digest:
        violations.append("observed_image_digest_must_match_release")
    fingerprint = expected.get("config_sha256")
    if not isinstance(fingerprint, str) or not _FINGERPRINT.fullmatch(fingerprint):
        violations.append("expected_config_sha256_is_invalid")
    elif observed.get("config_sha256") != fingerprint:
        violations.append("observed_config_sha256_must_match_release")
    if observed.get("container_running") is not True:
        violations.append("candidate_container_must_be_running")
    if _timestamp(observed.get("observed_at")) is None:
        violations.append("observed_at_must_be_timezone_aware")
    return tuple(violations)


def candidate_runtime_identity_matches(expected: dict[str, object], observed: dict[str, object]) -> bool:
    return not candidate_runtime_identity_violations(expected, observed)


def _timestamp(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None and parsed.utcoffset() is not None else None
