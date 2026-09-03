from __future__ import annotations


def database_connection_budget_violations(colors: dict[str, object], *, database_max_connections: int, reserved_connections: int = 20) -> tuple[str, ...]:
    if not isinstance(database_max_connections, int) or isinstance(database_max_connections, bool) or database_max_connections < 1:
        raise ValueError("database max connections must be a positive integer")
    if not isinstance(reserved_connections, int) or isinstance(reserved_connections, bool) or reserved_connections < 0 or reserved_connections >= database_max_connections:
        raise ValueError("reserved connections must be non-negative and below database maximum")
    if not isinstance(colors, dict):
        return ("color_connection_plans_are_required",)

    violations: list[str] = []
    total_demand = 0
    for color in ("blue", "green"):
        plan = colors.get(color)
        if not isinstance(plan, dict):
            violations.append(f"{color}:connection_plan_is_required")
            continue
        replicas, pool_size = plan.get("replicas"), plan.get("pool_size")
        if not isinstance(replicas, int) or isinstance(replicas, bool) or replicas < 1:
            violations.append(f"{color}:replicas_must_be_positive")
            continue
        if not isinstance(pool_size, int) or isinstance(pool_size, bool) or pool_size < 1:
            violations.append(f"{color}:pool_size_must_be_positive")
            continue
        if plan.get("pooling_enabled") is not True:
            violations.append(f"{color}:connection_pooling_must_be_enabled")
        total_demand += replicas * pool_size
    usable_connections = database_max_connections - reserved_connections
    if total_demand > usable_connections:
        violations.append("dual_color_connection_demand_exceeds_database_budget")
    return tuple(violations)


def database_connection_budget_is_safe(colors: dict[str, object], **policy: object) -> bool:
    return not database_connection_budget_violations(colors, **policy)
