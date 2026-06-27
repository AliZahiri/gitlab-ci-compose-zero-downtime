from __future__ import annotations


def nginx_validation_warnings(plan: dict[str, object]) -> tuple[str, ...]:
    warnings: list[str] = []
    if not plan.get("rendered_config_path"):
        warnings.append("rendered_config_path_missing")
    if plan.get("validation_required") is not True:
        warnings.append("validation_must_be_required")
    if plan.get("reload_on_validation_failure") is True:
        warnings.append("must_not_reload_on_validation_failure")
    return tuple(warnings)


def nginx_validation_plan_is_safe(plan: dict[str, object]) -> bool:
    return not nginx_validation_warnings(plan)
