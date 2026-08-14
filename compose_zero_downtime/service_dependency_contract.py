from __future__ import annotations


def service_dependency_contract_violations(services: list[dict[str, object]]) -> tuple[str, ...]:
    if not services:
        return ("at_least_one_service_is_required",)
    violations: list[str] = []
    names: set[str] = set()
    for index, service in enumerate(services):
        name = service.get("name")
        if not isinstance(name, str) or not name.strip():
            violations.append(f"service_{index}:name_is_required")
        elif name in names:
            violations.append(f"service_{index}:name_must_be_unique")
        if isinstance(name, str):
            names.add(name)
        dependencies = service.get("critical_dependencies", [])
        if not isinstance(dependencies, list):
            violations.append(f"service_{index}:critical_dependencies_must_be_a_list")
            continue
        for dependency_index, dependency in enumerate(dependencies):
            if not isinstance(dependency, dict) or not isinstance(dependency.get("service"), str) or not dependency["service"].strip():
                violations.append(f"service_{index}:dependency_{dependency_index}:service_is_required")
                continue
            if dependency.get("condition") != "service_healthy":
                violations.append(f"service_{index}:dependency_{dependency_index}:must_wait_for_health")
            if dependency.get("restart") is not True:
                violations.append(f"service_{index}:dependency_{dependency_index}:restart_propagation_is_required")
    return tuple(violations)


def service_dependencies_are_safe(services: list[dict[str, object]]) -> bool:
    return not service_dependency_contract_violations(services)
