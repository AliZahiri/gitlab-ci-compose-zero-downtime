from __future__ import annotations


def rollback_window_warnings(*, keep_old_seconds: int, smoke_check_seconds: int, min_observation_seconds: int = 120) -> tuple[str, ...]:
    warnings: list[str] = []
    if keep_old_seconds <= 0:
        warnings.append("keep_old_seconds_must_be_positive")
    if smoke_check_seconds <= 0:
        warnings.append("smoke_check_seconds_must_be_positive")
    if keep_old_seconds < smoke_check_seconds + min_observation_seconds:
        warnings.append("rollback_window_too_short")
    return tuple(warnings)


def rollback_window_is_safe(*, keep_old_seconds: int, smoke_check_seconds: int, min_observation_seconds: int = 120) -> bool:
    return not rollback_window_warnings(keep_old_seconds=keep_old_seconds, smoke_check_seconds=smoke_check_seconds, min_observation_seconds=min_observation_seconds)
