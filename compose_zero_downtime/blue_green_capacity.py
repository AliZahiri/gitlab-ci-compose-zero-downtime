from __future__ import annotations

from math import isfinite


def blue_green_capacity_violations(evidence: dict[str, object], *, minimum_healthy_replicas: int = 2, required_connection_headroom_ratio: float = 0.20) -> tuple[str, ...]:
    if not isinstance(minimum_healthy_replicas, int) or isinstance(minimum_healthy_replicas, bool) or minimum_healthy_replicas < 1:
        raise ValueError("minimum healthy replicas must be a positive integer")
    if not isinstance(required_connection_headroom_ratio, (int, float)) or isinstance(required_connection_headroom_ratio, bool) or not isfinite(float(required_connection_headroom_ratio)) or not 0 <= float(required_connection_headroom_ratio) < 1:
        raise ValueError("required connection headroom ratio must be finite and between zero and one")

    violations: list[str] = []
    active_color, candidate_color = evidence.get("active_color"), evidence.get("candidate_color")
    if not isinstance(active_color, str) or not active_color.strip():
        violations.append("active_color_is_required")
    if not isinstance(candidate_color, str) or not candidate_color.strip():
        violations.append("candidate_color_is_required")
    elif candidate_color == active_color:
        violations.append("candidate_color_must_differ_from_active_color")
    for field in ("active_healthy_replicas", "candidate_healthy_replicas"):
        count = evidence.get(field)
        if not isinstance(count, int) or isinstance(count, bool) or count < minimum_healthy_replicas:
            violations.append(f"{field}_is_below_minimum")
    expected = evidence.get("expected_peak_connections")
    available = evidence.get("candidate_available_connections")
    if not isinstance(expected, int) or isinstance(expected, bool) or expected < 1:
        violations.append("expected_peak_connections_must_be_positive")
    if not isinstance(available, int) or isinstance(available, bool) or available < 1:
        violations.append("candidate_available_connections_must_be_positive")
    elif isinstance(expected, int) and not isinstance(expected, bool) and available < expected * (1 + required_connection_headroom_ratio):
        violations.append("candidate_connection_headroom_is_insufficient")
    if evidence.get("rollback_capacity_reserved") is not True:
        violations.append("rollback_capacity_must_be_reserved")
    if evidence.get("candidate_health_quorum_met") is not True:
        violations.append("candidate_health_quorum_must_be_met")
    return tuple(violations)


def blue_green_capacity_is_ready(evidence: dict[str, object], **policy: object) -> bool:
    return not blue_green_capacity_violations(evidence, **policy)
