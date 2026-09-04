from __future__ import annotations

from datetime import datetime


def restart_stability_violations(evidence: dict[str, object], *, expected_containers: frozenset[str], now: datetime, maximum_restart_increase: int = 0, maximum_age_seconds: int = 300) -> tuple[str, ...]:
    if not isinstance(expected_containers, frozenset) or not expected_containers or any(not isinstance(value, str) or not value.strip() for value in expected_containers):
        raise ValueError("expected_containers must be a non-empty frozenset")
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("current time must be timezone-aware")
    if not isinstance(maximum_restart_increase, int) or isinstance(maximum_restart_increase, bool) or maximum_restart_increase < 0:
        raise ValueError("maximum_restart_increase must be non-negative")
    if not isinstance(maximum_age_seconds, int) or isinstance(maximum_age_seconds, bool) or maximum_age_seconds < 1:
        raise ValueError("maximum_age_seconds must be positive")
    containers = evidence.get("containers") if isinstance(evidence, dict) else None
    if not isinstance(containers, dict):
        return ("container_stability_evidence_is_required",)

    violations: list[str] = []
    if set(containers) != expected_containers:
        violations.append("observed_container_set_does_not_match_expected")
    for name in sorted(expected_containers):
        state = containers.get(name)
        if not isinstance(state, dict):
            violations.append(f"{name}:stability_state_is_required")
            continue
        baseline, current = state.get("baseline_restart_count"), state.get("current_restart_count")
        if any(not isinstance(value, int) or isinstance(value, bool) or value < 0 for value in (baseline, current)):
            violations.append(f"{name}:restart_counts_must_be_non_negative_integers")
        elif current < baseline or current - baseline > maximum_restart_increase:
            violations.append(f"{name}:restart_increase_exceeds_budget")
        if state.get("running") is not True:
            violations.append(f"{name}:must_be_running")
        if state.get("oom_killed") is not False:
            violations.append(f"{name}:must_not_be_oom_killed")
    observed_at = _timestamp(evidence.get("observed_at"))
    if observed_at is None or not 0 <= (now - observed_at).total_seconds() <= maximum_age_seconds:
        violations.append("restart_stability_observation_is_invalid_stale_or_future_dated")
    return tuple(violations)


def candidate_restart_stability_is_safe(evidence: dict[str, object], **policy: object) -> bool:
    return not restart_stability_violations(evidence, **policy)


def _timestamp(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None and parsed.utcoffset() is not None else None
