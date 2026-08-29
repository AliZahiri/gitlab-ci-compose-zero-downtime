from __future__ import annotations

from datetime import datetime
from math import isfinite


def promotion_soak_violations(evidence: dict[str, object], *, minimum_soak_seconds: int = 900, minimum_requests: int = 100, maximum_error_rate: float = 0.01, maximum_p95_ms: float = 1000.0) -> tuple[str, ...]:
    for name, value in (("minimum_soak_seconds", minimum_soak_seconds), ("minimum_requests", minimum_requests)):
        if not isinstance(value, int) or isinstance(value, bool) or value < 1:
            raise ValueError(f"{name} must be a positive integer")
    if not _probability(maximum_error_rate):
        raise ValueError("maximum_error_rate must be a probability")
    if not _finite_non_negative(maximum_p95_ms) or maximum_p95_ms == 0:
        raise ValueError("maximum_p95_ms must be positive and finite")
    violations: list[str] = []
    promoted_at, observed_at = _timestamp(evidence.get("promoted_at")), _timestamp(evidence.get("observed_at"))
    if promoted_at is None or observed_at is None:
        violations.append("promotion_timestamps_must_be_timezone_aware")
    elif (observed_at - promoted_at).total_seconds() < minimum_soak_seconds:
        violations.append("promotion_soak_window_is_incomplete")
    requests = evidence.get("request_count")
    errors = evidence.get("error_count")
    if not isinstance(requests, int) or isinstance(requests, bool) or requests < minimum_requests:
        violations.append("request_count_is_below_soak_minimum")
    if not isinstance(errors, int) or isinstance(errors, bool) or errors < 0:
        violations.append("error_count_must_be_non_negative")
    elif isinstance(requests, int) and not isinstance(requests, bool) and requests > 0 and errors / requests > maximum_error_rate:
        violations.append("promotion_error_rate_exceeds_budget")
    p95 = evidence.get("p95_latency_ms")
    if not _finite_non_negative(p95):
        violations.append("p95_latency_ms_must_be_finite_and_non_negative")
    elif p95 > maximum_p95_ms:
        violations.append("promotion_p95_latency_exceeds_budget")
    if evidence.get("rollback_triggered") is not False:
        violations.append("rollback_signal_must_be_clear")
    if evidence.get("old_color_available") is not True:
        violations.append("old_color_must_remain_available_during_soak")
    return tuple(violations)


def promotion_soak_is_complete(evidence: dict[str, object], **policy: object) -> bool:
    return not promotion_soak_violations(evidence, **policy)


def _finite_non_negative(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and isfinite(float(value)) and value >= 0


def _probability(value: object) -> bool:
    return _finite_non_negative(value) and value <= 1


def _timestamp(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None and parsed.utcoffset() is not None else None
