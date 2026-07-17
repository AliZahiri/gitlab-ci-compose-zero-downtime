from __future__ import annotations


def consecutive_healthy_samples(samples: list[bool] | tuple[bool, ...]) -> int:
    count = 0
    for sample in reversed(samples):
        if not sample:
            break
        count += 1
    return count


def promotion_window_is_satisfied(samples: list[bool] | tuple[bool, ...], *, required_samples: int = 3) -> bool:
    if required_samples <= 0:
        raise ValueError("required samples must be positive")
    return consecutive_healthy_samples(samples) >= required_samples
