from __future__ import annotations

from compose_zero_downtime.promotion_window import promotion_window_is_satisfied
from compose_zero_downtime.release_health_budget import release_health_warnings
from compose_zero_downtime.traffic_checkpoint import traffic_checkpoint_violations


def promotion_gate_violations(*, checkpoint: dict[str, object], health_samples: list[bool] | tuple[bool, ...], health_summary: dict[str, object], required_samples: int = 3, max_failures: int = 0, min_successes: int = 1) -> tuple[str, ...]:
    violations = list(traffic_checkpoint_violations(checkpoint))
    if not promotion_window_is_satisfied(health_samples, required_samples=required_samples):
        violations.append("promotion_health_window_not_satisfied")
    violations.extend(release_health_warnings(health_summary, max_failures=max_failures, min_successes=min_successes))
    return tuple(violations)


def promotion_is_ready(**inputs: object) -> bool:
    return not promotion_gate_violations(**inputs)
