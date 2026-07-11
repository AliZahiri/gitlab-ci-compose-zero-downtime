from __future__ import annotations


def deployment_allowed(current_hour_utc: int, frozen_hours_utc: set[int], *, emergency_override: bool = False) -> bool:
    if not 0 <= current_hour_utc <= 23:
        raise ValueError("current hour must be between 0 and 23")
    invalid_hours = [hour for hour in frozen_hours_utc if not 0 <= hour <= 23]
    if invalid_hours:
        raise ValueError("frozen hours must be between 0 and 23")
    return emergency_override or current_hour_utc not in frozen_hours_utc


def freeze_window_reason(current_hour_utc: int, frozen_hours_utc: set[int]) -> str | None:
    if deployment_allowed(current_hour_utc, frozen_hours_utc):
        return None
    return f"deployment blocked by freeze window at hour {current_hour_utc:02d}:00 UTC"
