from __future__ import annotations


def rollback_window_warnings(*, smoke_seconds: int, observation_seconds: int, minimum_seconds: int = 300) -> tuple[str, ...]:
    warnings: list[str] = []
    if smoke_seconds < 0 or observation_seconds < 0:
        warnings.append("durations_must_be_non_negative")
    if smoke_seconds + observation_seconds < minimum_seconds:
        warnings.append("rollback_window_too_short")
    return tuple(warnings)


def rollback_window_is_safe(*, smoke_seconds: int, observation_seconds: int, minimum_seconds: int = 300) -> bool:
    return not rollback_window_warnings(
        smoke_seconds=smoke_seconds,
        observation_seconds=observation_seconds,
        minimum_seconds=minimum_seconds,
    )
