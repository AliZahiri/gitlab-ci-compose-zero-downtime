from __future__ import annotations

from datetime import datetime


def artifact_age_violations(artifact: dict[str, object], *, now: datetime, max_age_seconds: int = 3600) -> tuple[str, ...]:
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("current time must be timezone-aware")
    if not isinstance(max_age_seconds, int) or isinstance(max_age_seconds, bool) or max_age_seconds <= 0:
        raise ValueError("maximum artifact age must be positive")
    observed = artifact.get("built_at")
    try:
        built_at = datetime.fromisoformat(observed.replace("Z", "+00:00")) if isinstance(observed, str) else None
    except ValueError:
        built_at = None
    violations: list[str] = []
    if built_at is None or built_at.tzinfo is None or built_at.utcoffset() is None:
        violations.append("built_at_must_be_timezone_aware")
    elif not 0 <= (now - built_at).total_seconds() <= max_age_seconds:
        violations.append("artifact_is_outside_age_budget")
    if not isinstance(artifact.get("digest"), str) or not artifact["digest"].startswith("sha256:"):
        violations.append("artifact_digest_must_be_immutable")
    return tuple(violations)


def artifact_is_current(artifact: dict[str, object], **policy: object) -> bool:
    return not artifact_age_violations(artifact, **policy)
