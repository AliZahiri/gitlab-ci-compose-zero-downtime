from __future__ import annotations

from ipaddress import ip_address


def blue_green_port_binding_violations(bindings: object) -> tuple[str, ...]:
    """Validate distinct loopback-only bindings for blue/green candidates."""
    if not isinstance(bindings, list) or not bindings:
        return ("bindings_must_be_a_non_empty_list",)

    violations: list[str] = []
    seen_colors: set[str] = set()
    seen_ports: set[int] = set()
    for index, binding in enumerate(bindings):
        if not isinstance(binding, dict):
            violations.append(f"binding_{index}:must_be_an_object")
            continue
        color = binding.get("color")
        if color not in {"blue", "green"}:
            violations.append(f"binding_{index}:color_must_be_blue_or_green")
        elif color in seen_colors:
            violations.append(f"binding_{index}:color_must_be_unique")
        else:
            seen_colors.add(color)

        host = binding.get("host")
        try:
            address = ip_address(host) if isinstance(host, str) else None
        except ValueError:
            address = None
        if address is None or not address.is_loopback:
            violations.append(f"binding_{index}:host_must_be_a_loopback_address")

        port = binding.get("port")
        if not isinstance(port, int) or isinstance(port, bool) or not 1 <= port <= 65535:
            violations.append(f"binding_{index}:port_must_be_between_1_and_65535")
        elif port in seen_ports:
            violations.append(f"binding_{index}:port_must_be_unique")
        else:
            seen_ports.add(port)

    for color in ("blue", "green"):
        if color not in seen_colors:
            violations.append(f"{color}_binding_is_required")
    return tuple(violations)


def blue_green_port_bindings_are_safe(bindings: object) -> bool:
    return not blue_green_port_binding_violations(bindings)
