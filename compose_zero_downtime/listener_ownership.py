from __future__ import annotations

from datetime import datetime
import re


_CONTAINER_ID = re.compile(r"[0-9a-f]{12,64}\Z")


def _timestamp(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None and parsed.utcoffset() is not None else None


def listener_ownership_violations(listeners: list[dict[str, object]], *, expected_project: str, now: datetime, maximum_age_seconds: int = 300) -> tuple[str, ...]:
    if not isinstance(expected_project, str) or not expected_project.strip():
        raise ValueError("expected project is required")
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("current time must be timezone-aware")
    if not isinstance(maximum_age_seconds, int) or isinstance(maximum_age_seconds, bool) or maximum_age_seconds < 0:
        raise ValueError("maximum age must be a non-negative integer")
    if not isinstance(listeners, list) or not listeners:
        return ("listener_evidence_is_required",)
    violations: list[str] = []
    colors: set[str] = set()
    endpoints: set[tuple[str, int]] = set()
    for index, listener in enumerate(listeners):
        if not isinstance(listener, dict):
            violations.append(f"listener_{index}:must_be_an_object")
            continue
        color = listener.get("color")
        if color not in {"blue", "green"}:
            violations.append(f"listener_{index}:color_is_invalid")
        elif color in colors:
            violations.append(f"listener_{index}:color_must_be_unique")
        else:
            colors.add(color)
        host, port = listener.get("host"), listener.get("port")
        if not isinstance(host, str) or not host.strip() or not isinstance(port, int) or isinstance(port, bool) or not 1 <= port <= 65535:
            violations.append(f"listener_{index}:endpoint_is_invalid")
        elif (host, port) in endpoints:
            violations.append(f"listener_{index}:endpoint_must_be_unique")
        else:
            endpoints.add((host, port))
        if listener.get("project_name") != expected_project:
            violations.append(f"listener_{index}:project_owner_does_not_match")
        container_id = listener.get("container_id")
        if not isinstance(container_id, str) or not _CONTAINER_ID.fullmatch(container_id):
            violations.append(f"listener_{index}:container_id_is_invalid")
        if listener.get("listening") is not True:
            violations.append(f"listener_{index}:socket_must_be_listening")
        observed_at = _timestamp(listener.get("observed_at"))
        if observed_at is None or not 0 <= (now - observed_at).total_seconds() <= maximum_age_seconds:
            violations.append(f"listener_{index}:observation_is_stale_or_invalid")
    for color in ("blue", "green"):
        if color not in colors:
            violations.append(f"{color}_listener_is_required")
    return tuple(violations)


def candidate_listeners_are_owned(listeners: list[dict[str, object]], **policy: object) -> bool:
    return not listener_ownership_violations(listeners, **policy)
