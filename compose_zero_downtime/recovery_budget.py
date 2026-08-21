from __future__ import annotations

from datetime import datetime


def recovery_budget_violations(report: dict[str, object]) -> tuple[str, ...]:
    violations: list[str] = []
    budget = report.get("max_recovery_seconds")
    observed = report.get("observed_recovery_seconds")
    if not isinstance(budget, int) or isinstance(budget, bool) or budget < 1:
        violations.append("max_recovery_seconds_must_be_positive")
    if not isinstance(observed, int) or isinstance(observed, bool) or observed < 0:
        violations.append("observed_recovery_seconds_must_be_non_negative")
    elif isinstance(budget, int) and not isinstance(budget, bool) and budget > 0 and observed > budget:
        violations.append("recovery_duration_exceeds_budget")
    if report.get("previous_target_healthy") is not True:
        violations.append("previous_target_health_must_be_confirmed")
    if report.get("rollback_completed") is not True:
        violations.append("rollback_must_complete")
    if _parse_timestamp(report.get("observed_at")) is None:
        violations.append("observed_at_must_be_timezone_aware")
    return tuple(violations)


def recovery_is_within_budget(report: dict[str, object]) -> bool:
    return not recovery_budget_violations(report)


def _parse_timestamp(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None and parsed.utcoffset() is not None else None
