from __future__ import annotations

from datetime import datetime
import re


_IDENTIFIER = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}\Z")
_SHA256 = re.compile(r"[0-9a-fA-F]{64}\Z")


def _timestamp(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None and parsed.utcoffset() is not None else None


def migration_backup_evidence_violations(evidence: dict[str, object], *, now: datetime, maximum_age_seconds: int = 3600) -> tuple[str, ...]:
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("current time must be timezone-aware")
    if not isinstance(maximum_age_seconds, int) or isinstance(maximum_age_seconds, bool) or maximum_age_seconds <= 0:
        raise ValueError("maximum evidence age must be a positive integer")

    violations: list[str] = []
    for field in ("migration_id", "backup_id"):
        value = evidence.get(field)
        if not isinstance(value, str) or not _IDENTIFIER.fullmatch(value):
            violations.append(f"{field}_is_invalid")
    digest = evidence.get("backup_sha256")
    if not isinstance(digest, str) or not _SHA256.fullmatch(digest):
        violations.append("backup_sha256_is_invalid")
    if evidence.get("backup_encrypted") is not True:
        violations.append("backup_must_be_encrypted")
    if evidence.get("restore_verified") is not True:
        violations.append("restore_must_be_verified")

    for field in ("backup_completed_at", "restore_verified_at"):
        observed = _timestamp(evidence.get(field))
        if observed is None:
            violations.append(f"{field}_must_be_timezone_aware")
            continue
        age = (now - observed).total_seconds()
        if age < 0:
            violations.append(f"{field}_is_in_the_future")
        elif age > maximum_age_seconds:
            violations.append(f"{field}_is_stale")
    return tuple(violations)


def migration_backup_evidence_is_ready(evidence: dict[str, object], **policy: object) -> bool:
    return not migration_backup_evidence_violations(evidence, **policy)
