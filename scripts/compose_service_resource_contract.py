from __future__ import annotations


def compose_service_resource_violations(services: object, *, minimum_memory_mib: int = 64, maximum_readiness_seconds: int = 300) -> tuple[str, ...]:
    if not isinstance(minimum_memory_mib, int) or isinstance(minimum_memory_mib, bool) or minimum_memory_mib < 1:
        raise ValueError("minimum_memory_mib must be a positive integer")
    if not isinstance(maximum_readiness_seconds, int) or isinstance(maximum_readiness_seconds, bool) or maximum_readiness_seconds < 1:
        raise ValueError("maximum_readiness_seconds must be a positive integer")
    if not isinstance(services, list) or not services:
        return ("at_least_one_service_contract_is_required",)
    violations: list[str] = []
    names: set[str] = set()
    for index, service in enumerate(services):
        prefix = f"service_{index}"
        if not isinstance(service, dict):
            violations.append(f"{prefix}:must_be_an_object")
            continue
        name = service.get("name")
        if not isinstance(name, str) or not name.strip():
            violations.append(f"{prefix}:name_is_required")
        elif name in names:
            violations.append(f"{prefix}:name_must_be_unique")
        else:
            names.add(name)
        cpu = service.get("cpu_limit")
        if not isinstance(cpu, (int, float)) or isinstance(cpu, bool) or cpu <= 0:
            violations.append(f"{prefix}:cpu_limit_must_be_positive")
        memory = service.get("memory_limit_mib")
        if not isinstance(memory, int) or isinstance(memory, bool) or memory < minimum_memory_mib:
            violations.append(f"{prefix}:memory_limit_is_below_policy")
        if service.get("restart") not in {"unless-stopped", "on-failure"}:
            violations.append(f"{prefix}:restart_policy_is_not_approved")
        readiness = service.get("readiness_timeout_seconds")
        if not isinstance(readiness, int) or isinstance(readiness, bool) or not 1 <= readiness <= maximum_readiness_seconds:
            violations.append(f"{prefix}:readiness_timeout_is_out_of_policy")
    return tuple(violations)


def compose_service_resources_are_ready(services: object, **policy: object) -> bool:
    return not compose_service_resource_violations(services, **policy)
