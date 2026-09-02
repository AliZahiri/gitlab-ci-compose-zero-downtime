from __future__ import annotations


def nginx_worker_drain_violations(samples: list[dict[str, object]], *, maximum_drain_seconds: int = 60) -> tuple[str, ...]:
    if not isinstance(maximum_drain_seconds, int) or isinstance(maximum_drain_seconds, bool) or maximum_drain_seconds < 1:
        raise ValueError("maximum_drain_seconds must be a positive integer")
    if not isinstance(samples, list) or len(samples) < 2:
        return ("at_least_two_drain_samples_are_required",)
    violations: list[str] = []
    elapsed: list[int] = []
    connections: list[int] = []
    for index, sample in enumerate(samples):
        seconds, active = sample.get("elapsed_seconds"), sample.get("old_worker_active_connections")
        if not isinstance(seconds, int) or isinstance(seconds, bool) or seconds < 0:
            violations.append(f"sample_{index}:elapsed_seconds_must_be_non_negative")
        else:
            elapsed.append(seconds)
        if not isinstance(active, int) or isinstance(active, bool) or active < 0:
            violations.append(f"sample_{index}:active_connections_must_be_non_negative")
        else:
            connections.append(active)
        if sample.get("candidate_upstream_healthy") is not True:
            violations.append(f"sample_{index}:candidate_upstream_must_be_healthy")
        if sample.get("rollback_ready") is not True:
            violations.append(f"sample_{index}:rollback_must_remain_ready")
    if len(elapsed) == len(samples) and (elapsed != sorted(elapsed) or len(set(elapsed)) != len(elapsed)):
        violations.append("sample_elapsed_seconds_must_increase")
    if len(connections) == len(samples) and any(current > previous for previous, current in zip(connections, connections[1:])):
        violations.append("old_worker_connections_must_not_increase")
    if connections and connections[-1] != 0:
        violations.append("old_worker_connections_must_reach_zero")
    if elapsed and elapsed[-1] > maximum_drain_seconds:
        violations.append("worker_drain_budget_exceeded")
    return tuple(violations)


def nginx_workers_are_drained(samples: list[dict[str, object]], **policy: object) -> bool:
    return not nginx_worker_drain_violations(samples, **policy)
