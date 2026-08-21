from __future__ import annotations

from datetime import datetime


def migration_execution_evidence_violations(
    evidence: dict[str, object], *, maximum_duration_seconds: int = 300
) -> tuple[str, ...]:
    if (
        not isinstance(maximum_duration_seconds, int)
        or isinstance(maximum_duration_seconds, bool)
        or maximum_duration_seconds < 1
    ):
        raise ValueError("maximum duration must be a positive integer")

    violations: list[str] = []
    for field in ("migration_id", "release_id"):
        if not isinstance(evidence.get(field), str) or not evidence[field].strip():
            violations.append(f"{field}_is_required")
    duration = evidence.get("duration_seconds")
    if not isinstance(duration, int) or isinstance(duration, bool) or duration < 0:
        violations.append("duration_seconds_must_be_non_negative")
    elif duration > maximum_duration_seconds:
        violations.append("migration_duration_exceeds_budget")
    if evidence.get("backward_compatible") is not True:
        violations.append("migration_must_be_backward_compatible")
    if evidence.get("lock_wait_exceeded") is not False:
        violations.append("migration_lock_wait_must_not_exceed_budget")
    if _parse_timestamp(evidence.get("completed_at")) is None:
        violations.append("completed_at_must_be_timezone_aware")
    return tuple(violations)


def migration_execution_evidence_is_safe(
    evidence: dict[str, object], *, maximum_duration_seconds: int = 300
) -> bool:
    return not migration_execution_evidence_violations(
        evidence, maximum_duration_seconds=maximum_duration_seconds
    )


def _parse_timestamp(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None and parsed.utcoffset() is not None else None
