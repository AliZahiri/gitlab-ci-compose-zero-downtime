from __future__ import annotations

from datetime import datetime


_REQUIRED_STAGES = ("deploy", "proxy_switch", "smoke_test")


def deployment_log_correlation_violations(events: list[dict[str, object]]) -> tuple[str, ...]:
    if not isinstance(events, list) or not events:
        return ("deployment_events_are_required",)
    violations: list[str] = []
    stages: set[str] = set()
    release_ids: set[str] = set()
    correlation_ids: set[str] = set()
    timestamps: list[datetime] = []
    for index, event in enumerate(events):
        stage = event.get("stage") if isinstance(event, dict) else None
        if not isinstance(stage, str) or not stage.strip():
            violations.append(f"event_{index}:stage_is_required")
        elif stage in stages:
            violations.append(f"event_{index}:stage_must_be_unique")
        else:
            stages.add(stage)
        for field, target in (("release_id", release_ids), ("correlation_id", correlation_ids)):
            value = event.get(field) if isinstance(event, dict) else None
            if not isinstance(value, str) or not value.strip():
                violations.append(f"event_{index}:{field}_is_required")
            else:
                target.add(value)
        observed_at = _timestamp(event.get("observed_at") if isinstance(event, dict) else None)
        if observed_at is None:
            violations.append(f"event_{index}:observed_at_must_be_timezone_aware")
        else:
            timestamps.append(observed_at)
        if isinstance(event, dict) and event.get("status") != "succeeded":
            violations.append(f"event_{index}:status_must_be_succeeded")
    for stage in _REQUIRED_STAGES:
        if stage not in stages:
            violations.append(f"required_stage_{stage}_is_missing")
    if len(release_ids) != 1:
        violations.append("events_must_share_one_release_id")
    if len(correlation_ids) != 1:
        violations.append("events_must_share_one_correlation_id")
    if len(timestamps) == len(events) and timestamps != sorted(timestamps):
        violations.append("event_timestamps_must_be_ordered")
    return tuple(violations)


def deployment_logs_are_correlated(events: list[dict[str, object]]) -> bool:
    return not deployment_log_correlation_violations(events)


def _timestamp(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None and parsed.utcoffset() is not None else None
