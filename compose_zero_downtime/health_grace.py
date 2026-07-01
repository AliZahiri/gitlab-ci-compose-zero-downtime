from __future__ import annotations


def health_grace_warnings(*, warmup_seconds: int, interval_seconds: int, max_grace_seconds: int = 180) -> tuple[str, ...]:
    warnings: list[str] = []
    if warmup_seconds <= 0:
        warnings.append("warmup_seconds_must_be_positive")
    if interval_seconds <= 0:
        warnings.append("interval_seconds_must_be_positive")
    if warmup_seconds > max_grace_seconds:
        warnings.append("warmup_exceeds_max_grace")
    if interval_seconds > 0 and warmup_seconds > 0 and warmup_seconds < interval_seconds:
        warnings.append("warmup_shorter_than_interval")
    return tuple(warnings)


def health_grace_is_safe(*, warmup_seconds: int, interval_seconds: int, max_grace_seconds: int = 180) -> bool:
    return not health_grace_warnings(warmup_seconds=warmup_seconds, interval_seconds=interval_seconds, max_grace_seconds=max_grace_seconds)
