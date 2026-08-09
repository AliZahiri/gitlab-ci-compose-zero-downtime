from __future__ import annotations

from math import isfinite


def shutdown_budget_violations(services: list[dict[str, object]], *, safety_margin_seconds: float = 5.0) -> tuple[str, ...]:
    if not isinstance(safety_margin_seconds, (int, float)) or isinstance(safety_margin_seconds, bool) or not isfinite(float(safety_margin_seconds)) or safety_margin_seconds < 0:
        raise ValueError("safety margin must be a finite non-negative number")
    if not services:
        return ("at_least_one_shutdown_observation_is_required",)
    violations: list[str] = []
    seen: set[str] = set()
    for position, service in enumerate(services):
        name = str(service.get("service", "")).strip()
        if not name:
            violations.append(f"service_{position}:name_is_required")
        elif name in seen:
            violations.append(f"service_{position}:name_must_be_unique")
        seen.add(name)
        if service.get("stop_signal") != "SIGTERM":
            violations.append(f"service_{position}:stop_signal_must_be_sigterm")
        values: dict[str, float] = {}
        for field in ("drain_seconds", "termination_seconds", "stop_grace_period_seconds"):
            value = service.get(field)
            if not isinstance(value, (int, float)) or isinstance(value, bool) or not isfinite(float(value)) or value < 0:
                violations.append(f"service_{position}:{field}_must_be_finite_and_non_negative")
            else:
                values[field] = float(value)
        if len(values) == 3 and values["stop_grace_period_seconds"] < values["drain_seconds"] + values["termination_seconds"] + float(safety_margin_seconds):
            violations.append(f"service_{position}:stop_grace_period_below_shutdown_budget")
    return tuple(violations)


def shutdown_budget_is_safe(services: list[dict[str, object]], **policy: object) -> bool:
    return not shutdown_budget_violations(services, **policy)
