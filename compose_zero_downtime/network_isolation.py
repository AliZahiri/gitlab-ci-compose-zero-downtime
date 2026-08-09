from __future__ import annotations


def compose_network_isolation_violations(services: dict[str, dict[str, object]], *, public_network: str = "edge", private_network: str = "backend") -> tuple[str, ...]:
    if not public_network.strip() or not private_network.strip() or public_network == private_network:
        raise ValueError("public and private networks must be distinct non-empty names")
    if not services:
        return ("at_least_one_service_is_required",)
    violations: list[str] = []
    roles_seen: set[str] = set()
    for name, service in services.items():
        if not str(name).strip() or not isinstance(service, dict):
            violations.append("service_entries_must_have_names_and_mappings")
            continue
        role = service.get("role")
        if role not in {"proxy", "workload", "data"}:
            violations.append(f"service:{name}:role_is_invalid")
            continue
        roles_seen.add(str(role))
        networks = service.get("networks")
        if not isinstance(networks, list) or not networks or any(not isinstance(value, str) or not value.strip() for value in networks):
            violations.append(f"service:{name}:networks_must_be_non_empty_names")
            continue
        if len(networks) != len(set(networks)):
            violations.append(f"service:{name}:networks_must_be_unique")
        network_set = set(networks)
        ports = service.get("published_ports", [])
        if not isinstance(ports, list):
            violations.append(f"service:{name}:published_ports_must_be_a_list")
            ports = []
        if role == "proxy" and not {public_network, private_network}.issubset(network_set):
            violations.append(f"service:{name}:proxy_must_join_public_and_private_networks")
        if role in {"workload", "data"}:
            if private_network not in network_set or public_network in network_set:
                violations.append(f"service:{name}:{role}_must_be_private_only")
            if ports:
                violations.append(f"service:{name}:{role}_must_not_publish_ports")
    if "proxy" not in roles_seen or "workload" not in roles_seen:
        violations.append("proxy_and_workload_roles_are_required")
    return tuple(violations)


def compose_network_isolation_is_safe(services: dict[str, dict[str, object]], **policy: object) -> bool:
    return not compose_network_isolation_violations(services, **policy)
