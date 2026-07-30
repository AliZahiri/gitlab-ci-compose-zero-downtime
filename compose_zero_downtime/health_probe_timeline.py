from __future__ import annotations

from datetime import datetime


def _timestamp(value: object) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None and parsed.utcoffset() is not None else None


def health_probe_timeline_violations(samples: list[dict[str, object]], *, now: datetime, required_consecutive: int = 3, maximum_interval_seconds: int = 30, maximum_age_seconds: int = 60) -> tuple[str, ...]:
    for name, value in (("required consecutive samples", required_consecutive), ("maximum interval seconds", maximum_interval_seconds), ("maximum age seconds", maximum_age_seconds)):
        if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
            raise ValueError(f"{name} must be a positive integer")
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("current time must be timezone-aware")
    if not samples:
        return ("health_probe_samples_are_required",)
    violations: list[str] = []
    parsed: list[datetime | None] = []
    for index, sample in enumerate(samples):
        observed_at = _timestamp(sample.get("observed_at"))
        parsed.append(observed_at)
        if observed_at is None:
            violations.append(f"sample_{index}:observed_at_must_be_timezone_aware")
        if not isinstance(sample.get("healthy"), bool):
            violations.append(f"sample_{index}:healthy_must_be_boolean")
    for index in range(1, len(parsed)):
        previous, current = parsed[index - 1], parsed[index]
        if previous is not None and current is not None:
            interval = (current - previous).total_seconds()
            if interval <= 0:
                violations.append(f"sample_{index}:observations_must_be_strictly_increasing")
            elif interval > maximum_interval_seconds:
                violations.append(f"sample_{index}:observation_interval_exceeds_maximum")
    latest = parsed[-1]
    if latest is not None:
        age = (now - latest).total_seconds()
        if age < 0:
            violations.append("latest_health_observation_is_in_the_future")
        elif age > maximum_age_seconds:
            violations.append("latest_health_observation_is_stale")
    if len(samples) < required_consecutive or any(sample.get("healthy") is not True for sample in samples[-required_consecutive:]):
        violations.append("consecutive_healthy_sample_requirement_not_met")
    return tuple(violations)


def health_probe_timeline_is_promotable(**inputs: object) -> bool:
    return not health_probe_timeline_violations(**inputs)
