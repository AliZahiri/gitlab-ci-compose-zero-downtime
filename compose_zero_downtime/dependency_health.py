from __future__ import annotations


_ALLOWED_CONDITIONS = {"service_healthy", "service_completed_successfully"}


def dependency_health_violations(services: dict[str, object], *, promoted_service: str) -> tuple[str, ...]:
    if not isinstance(promoted_service, str) or not promoted_service.strip():
        raise ValueError("promoted service must be a non-empty string")
    if not isinstance(services, dict) or not services:
        return ("at_least_one_service_is_required",)

    violations: list[str] = []
    normalized: dict[str, object] = {}
    for raw_name, service in services.items():
        name = raw_name.strip() if isinstance(raw_name, str) else ""
        if not name:
            violations.append("service_name_is_required")
            continue
        if name in normalized:
            violations.append(f"service:{name}:name_must_be_unique")
            continue
        normalized[name] = service

    promoted = promoted_service.strip()
    if promoted not in normalized:
        violations.append("promoted_service_is_not_declared")

    graph: dict[str, set[str]] = {name: set() for name in normalized}
    for name, service in normalized.items():
        if not isinstance(service, dict):
            violations.append(f"service:{name}:metadata_is_required")
            continue
        if name == promoted and service.get("healthcheck_enabled") is not True:
            violations.append(f"service:{name}:healthcheck_must_be_enabled")
        dependencies = service.get("depends_on", {})
        if not isinstance(dependencies, dict):
            violations.append(f"service:{name}:depends_on_must_be_a_mapping")
            continue
        for raw_dependency, evidence in dependencies.items():
            dependency = raw_dependency.strip() if isinstance(raw_dependency, str) else ""
            if not dependency:
                violations.append(f"service:{name}:dependency_name_is_required")
                continue
            if dependency not in normalized:
                violations.append(f"service:{name}:dependency:{dependency}:is_not_declared")
                continue
            if dependency == name:
                violations.append(f"service:{name}:cannot_depend_on_itself")
                continue
            graph[name].add(dependency)
            condition = evidence.get("condition") if isinstance(evidence, dict) else None
            if condition == "service_started":
                violations.append(f"service:{name}:dependency:{dependency}:service_started_is_not_allowed")
            elif condition not in _ALLOWED_CONDITIONS:
                violations.append(f"service:{name}:dependency:{dependency}:condition_must_be_explicit_and_health_gated")

    visiting: set[str] = set()
    visited: set[str] = set()

    def has_cycle(name: str) -> bool:
        if name in visiting:
            return True
        if name in visited:
            return False
        visiting.add(name)
        cyclic = any(has_cycle(dependency) for dependency in graph[name])
        visiting.remove(name)
        visited.add(name)
        return cyclic

    if any(has_cycle(name) for name in graph):
        violations.append("dependency_cycle_detected")
    return tuple(violations)


def release_dependency_health_is_ready(services: dict[str, object], **policy: object) -> bool:
    return not dependency_health_violations(services, **policy)
