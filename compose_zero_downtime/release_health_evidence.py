from __future__ import annotations

from datetime import datetime


def release_health_evidence_violations(evidence: dict[str, object], *, now: datetime, max_age_seconds: int = 300) -> tuple[str, ...]:
    violations: list[str] = []
    observed_at = evidence.get("observed_at")
    if not isinstance(observed_at, str):
        return ("observed_at_must_be_timezone_aware",)
    try:
        timestamp = datetime.fromisoformat(observed_at.replace("Z", "+00:00"))
    except ValueError:
        return ("observed_at_must_be_timezone_aware",)
    if timestamp.tzinfo is None or timestamp.utcoffset() is None or now.tzinfo is None or now.utcoffset() is None:
        violations.append("observed_at_must_be_timezone_aware")
    elif (now - timestamp).total_seconds() < 0 or (now - timestamp).total_seconds() > max_age_seconds:
        violations.append("health_evidence_is_outside_age_budget")
    if evidence.get("candidate_color") not in {"blue", "green"}:
        violations.append("candidate_color_must_be_blue_or_green")
    if evidence.get("healthy") is not True:
        violations.append("candidate_health_must_pass")
    return tuple(violations)


def release_health_evidence_is_fresh(evidence: dict[str, object], *, now: datetime, max_age_seconds: int = 300) -> bool:
    return not release_health_evidence_violations(evidence, now=now, max_age_seconds=max_age_seconds)
