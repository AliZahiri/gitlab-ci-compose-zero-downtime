from __future__ import annotations


def rollback_reasons(*, healthy: bool, error_rate: float, maximum_error_rate: float, consecutive_failures: int, failure_threshold: int) -> tuple[str, ...]:
    if isinstance(error_rate, bool) or isinstance(maximum_error_rate, bool) or not 0 <= error_rate <= 1 or not 0 <= maximum_error_rate <= 1:
        raise ValueError("error rates must be between zero and one")
    if any(isinstance(value, bool) or not isinstance(value, int) or value < 0 for value in (consecutive_failures, failure_threshold)) or failure_threshold < 1:
        raise ValueError("failure counters require a positive threshold")
    reasons: list[str] = []
    if healthy is not True:
        reasons.append("candidate_is_unhealthy")
    if error_rate > maximum_error_rate:
        reasons.append("error_rate_budget_exceeded")
    if consecutive_failures >= failure_threshold:
        reasons.append("consecutive_failure_threshold_reached")
    return tuple(reasons)


def rollback_is_required(**observations: object) -> bool:
    return bool(rollback_reasons(**observations))
