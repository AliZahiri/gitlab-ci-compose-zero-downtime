from __future__ import annotations


def startup_budget_warnings(*, attempts: int, interval_seconds: float, max_seconds: float = 180.0) -> tuple[str, ...]:
    warnings: list[str] = []
    if attempts <= 0:
        warnings.append("attempts_must_be_positive")
    if interval_seconds <= 0:
        warnings.append("interval_seconds_must_be_positive")
    if attempts > 0 and interval_seconds > 0 and attempts * interval_seconds > max_seconds:
        warnings.append("startup_budget_exceeds_max_seconds")
    return tuple(warnings)


def startup_budget_is_safe(*, attempts: int, interval_seconds: float, max_seconds: float = 180.0) -> bool:
    return not startup_budget_warnings(attempts=attempts, interval_seconds=interval_seconds, max_seconds=max_seconds)
