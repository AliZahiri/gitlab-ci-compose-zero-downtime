from __future__ import annotations


def compose_dependency_restart_violations(services: object) -> tuple[str, ...]:
    if not isinstance(services, dict) or not services:
        return ("services_must_be_a_non_empty_object",)
    violations: list[str] = []
    for service_name, service in services.items():
        if not isinstance(service_name, str) or not service_name.strip() or not isinstance(service, dict):
            violations.append("service_names_and_definitions_must_be_valid")
            continue
        dependencies = service.get("depends_on", {})
        if not isinstance(dependencies, dict):
            violations.append(f"{service_name}:depends_on_must_use_long_form_mapping")
            continue
        for dependency_name, contract in dependencies.items():
            if dependency_name not in services:
                violations.append(f"{service_name}:{dependency_name}:dependency_is_not_declared")
                continue
            if dependency_name == service_name:
                violations.append(f"{service_name}:{dependency_name}:service_must_not_depend_on_itself")
                continue
            if not isinstance(contract, dict):
                violations.append(f"{service_name}:{dependency_name}:dependency_contract_must_be_an_object")
                continue
            if contract.get("condition") != "service_healthy":
                violations.append(f"{service_name}:{dependency_name}:dependency_must_be_health_gated")
            if contract.get("restart") is not True:
                violations.append(f"{service_name}:{dependency_name}:dependency_restart_must_be_enabled")
            if contract.get("required") is not True:
                violations.append(f"{service_name}:{dependency_name}:dependency_must_be_required")
    return tuple(violations)


def compose_dependency_restart_contract_is_safe(services: object) -> bool:
    return not compose_dependency_restart_violations(services)
