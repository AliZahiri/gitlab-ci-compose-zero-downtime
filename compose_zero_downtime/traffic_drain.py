from __future__ import annotations

from datetime import datetime


def _timestamp(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None and parsed.utcoffset() is not None else None


def traffic_drain_violations(observations: list[dict[str, object]], *, minimum_observations: int = 2, maximum_interval_seconds: int = 30, maximum_remaining_requests: int = 0) -> tuple[str, ...]:
    for name, value, allow_zero in (("minimum observations", minimum_observations, False), ("maximum interval seconds", maximum_interval_seconds, False), ("maximum remaining requests", maximum_remaining_requests, True)):
        if not isinstance(value, int) or isinstance(value, bool) or value < (0 if allow_zero else 1):
            raise ValueError(f"{name} policy is invalid")
    if len(observations) < minimum_observations:
        return ("traffic_drain_observations_are_insufficient",)
    violations: list[str] = []
    parsed: list[datetime | None] = []
    counts: list[int | None] = []
    for index, observation in enumerate(observations):
        observed_at = _timestamp(observation.get("observed_at"))
        parsed.append(observed_at)
        if observed_at is None:
            violations.append(f"observation_{index}:observed_at_must_be_timezone_aware")
        count = observation.get("in_flight_requests")
        valid_count = isinstance(count, int) and not isinstance(count, bool) and count >= 0
        counts.append(count if valid_count else None)
        if not valid_count:
            violations.append(f"observation_{index}:in_flight_requests_must_be_a_non_negative_integer")
    for index in range(1, len(observations)):
        if parsed[index - 1] is not None and parsed[index] is not None:
            interval = (parsed[index] - parsed[index - 1]).total_seconds()
            if interval <= 0:
                violations.append(f"observation_{index}:timestamps_must_be_strictly_increasing")
            elif interval > maximum_interval_seconds:
                violations.append(f"observation_{index}:sampling_interval_exceeds_maximum")
        if counts[index - 1] is not None and counts[index] is not None and counts[index] > counts[index - 1]:
            violations.append(f"observation_{index}:in_flight_requests_must_not_increase")
    if counts[-1] is not None and counts[-1] > maximum_remaining_requests:
        violations.append("traffic_drain_threshold_not_reached")
    return tuple(violations)


def old_color_is_safe_to_stop(observations: list[dict[str, object]], **policy: object) -> bool:
    return not traffic_drain_violations(observations, **policy)
