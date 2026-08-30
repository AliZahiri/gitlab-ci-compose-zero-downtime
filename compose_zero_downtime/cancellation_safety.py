from __future__ import annotations

from datetime import datetime


_OUTCOMES = frozenset({"candidate_stopped", "rollback_completed", "promotion_completed"})


def deployment_cancellation_violations(evidence: dict[str, object]) -> tuple[str, ...]:
    violations: list[str] = []
    if not isinstance(evidence.get("deployment_id"), str) or not evidence["deployment_id"].strip():
        violations.append("deployment_id_is_required")
    if _timestamp(evidence.get("cancelled_at")) is None:
        violations.append("cancelled_at_must_be_timezone_aware")
    traffic_switched = evidence.get("traffic_switched")
    if not isinstance(traffic_switched, bool):
        violations.append("traffic_switched_must_be_boolean")
    outcome = evidence.get("safe_outcome")
    if outcome not in _OUTCOMES:
        violations.append("safe_outcome_is_invalid")
    elif traffic_switched is True and outcome not in {"rollback_completed", "promotion_completed"}:
        violations.append("switched_traffic_requires_rollback_or_promotion_completion")
    elif traffic_switched is False and outcome != "candidate_stopped":
        violations.append("unswitched_candidate_must_be_stopped")
    if evidence.get("active_color_health_verified") is not True:
        violations.append("active_color_health_must_be_verified")
    if evidence.get("transition_journal_persisted") is not True:
        violations.append("transition_journal_must_be_persisted")
    if evidence.get("deployment_lock_released") is not True:
        violations.append("deployment_lock_must_be_released_after_safe_outcome")
    return tuple(violations)


def deployment_cancellation_is_safe(evidence: dict[str, object]) -> bool:
    return not deployment_cancellation_violations(evidence)


def _timestamp(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None and parsed.utcoffset() is not None else None
