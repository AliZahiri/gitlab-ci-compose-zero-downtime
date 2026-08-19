from __future__ import annotations

from datetime import datetime


def freeze_evidence_violations(evidence: dict[str, object], *, now: datetime, maximum_age_seconds: int = 900) -> tuple[str, ...]:
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("current time must be timezone-aware")
    if not isinstance(maximum_age_seconds, int) or isinstance(maximum_age_seconds, bool) or maximum_age_seconds <= 0:
        raise ValueError("maximum evidence age must be positive")
    violations: list[str] = []
    frozen = evidence.get("freeze_active")
    if not isinstance(frozen, bool):
        violations.append("freeze_active_must_be_boolean")
    deployment_type = evidence.get("deployment_type")
    if deployment_type not in {"standard", "emergency"}:
        violations.append("deployment_type_is_invalid")
    elif frozen is True and deployment_type != "emergency":
        violations.append("active_freeze_requires_emergency_deployment")
    if deployment_type == "emergency":
        for field in ("approval_reference", "approved_by", "emergency_reason"):
            if not isinstance(evidence.get(field), str) or not evidence[field].strip():
                violations.append(f"{field}_is_required_for_emergency")
    value = evidence.get("observed_at")
    try:
        timestamp = datetime.fromisoformat(value.replace("Z", "+00:00")) if isinstance(value, str) else None
    except ValueError:
        timestamp = None
    if timestamp is None or timestamp.tzinfo is None or timestamp.utcoffset() is None:
        violations.append("observed_at_must_be_timezone_aware")
    elif not 0 <= (now - timestamp).total_seconds() <= maximum_age_seconds:
        violations.append("freeze_evidence_is_not_fresh")
    return tuple(violations)


def deployment_has_freeze_clearance(evidence: dict[str, object], **policy: object) -> bool:
    return not freeze_evidence_violations(evidence, **policy)
