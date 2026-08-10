from __future__ import annotations


_REQUIRED_STAGES = ("pull", "startup", "health", "promotion")


def deployment_timeout_violations(budgets: dict[str, object], observations: dict[str, object]) -> tuple[str, ...]:
    violations: list[str] = []
    stage_budget_total = 0.0
    stage_observation_total = 0.0
    for stage in _REQUIRED_STAGES:
        budget = budgets.get(stage)
        observed = observations.get(stage)
        if not isinstance(budget, (int, float)) or isinstance(budget, bool) or budget <= 0:
            violations.append(f"{stage}:budget_must_be_positive")
            continue
        stage_budget_total += budget
        if not isinstance(observed, (int, float)) or isinstance(observed, bool) or observed < 0:
            violations.append(f"{stage}:observation_must_be_non_negative")
            continue
        stage_observation_total += observed
        if observed > budget:
            violations.append(f"{stage}:timeout_budget_exceeded")

    total_budget = budgets.get("total")
    if not isinstance(total_budget, (int, float)) or isinstance(total_budget, bool) or total_budget < stage_budget_total:
        violations.append("total:budget_must_cover_declared_stages")
    elif stage_observation_total > total_budget:
        violations.append("total:timeout_budget_exceeded")
    return tuple(violations)


def deployment_timeout_is_within_budget(budgets: dict[str, object], observations: dict[str, object]) -> bool:
    return not deployment_timeout_violations(budgets, observations)
