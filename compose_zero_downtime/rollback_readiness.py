from __future__ import annotations


def rollback_readiness_warnings(state: dict[str, object]) -> tuple[str, ...]:
    warnings: list[str] = []
    if state.get("previous_color_healthy") is not True:
        warnings.append("previous_color_is_not_healthy")
    if state.get("proxy_switch_ready") is not True:
        warnings.append("proxy_switch_is_not_ready")
    if not str(state.get("previous_color", "")).strip():
        warnings.append("previous_color_is_required")
    return tuple(warnings)


def rollback_is_ready(state: dict[str, object]) -> bool:
    return not rollback_readiness_warnings(state)
