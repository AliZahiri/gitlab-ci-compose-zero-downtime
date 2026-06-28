from __future__ import annotations


def disk_check_warnings(*, free_percent: float, min_free_percent: float = 15.0) -> tuple[str, ...]:
    if free_percent < 0 or free_percent > 100:
        return ("free_percent_must_be_between_0_and_100",)
    if free_percent < min_free_percent:
        return ("free_disk_below_deploy_threshold",)
    return ()


def disk_check_passes(*, free_percent: float, min_free_percent: float = 15.0) -> bool:
    return not disk_check_warnings(free_percent=free_percent, min_free_percent=min_free_percent)
