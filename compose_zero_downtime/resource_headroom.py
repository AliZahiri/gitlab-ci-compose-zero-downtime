from __future__ import annotations

from math import isfinite


def dual_color_headroom_violations(resources: dict[str, dict[str, object]], *, safety_margin_ratio: float = 0.20) -> tuple[str, ...]:
    if not isinstance(safety_margin_ratio, (int, float)) or isinstance(safety_margin_ratio, bool) or not isfinite(float(safety_margin_ratio)) or not 0 <= safety_margin_ratio < 1:
        raise ValueError("safety margin ratio must be finite and between zero and one")
    violations: list[str] = []
    for name in ("memory_mb", "disk_mb"):
        observation = resources.get(name)
        if not isinstance(observation, dict):
            violations.append(f"resource:{name}:observation_is_required")
            continue
        available = observation.get("available")
        required = observation.get("candidate_required")
        if not isinstance(available, (int, float)) or isinstance(available, bool) or not isfinite(float(available)) or available < 0:
            violations.append(f"resource:{name}:available_must_be_finite_and_non_negative")
            continue
        if not isinstance(required, (int, float)) or isinstance(required, bool) or not isfinite(float(required)) or required <= 0:
            violations.append(f"resource:{name}:candidate_required_must_be_finite_and_positive")
            continue
        if available * (1 - safety_margin_ratio) < required:
            violations.append(f"resource:{name}:dual_color_headroom_is_insufficient")
    return tuple(violations)


def host_has_dual_color_headroom(resources: dict[str, dict[str, object]], **policy: object) -> bool:
    return not dual_color_headroom_violations(resources, **policy)
