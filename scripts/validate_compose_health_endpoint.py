from __future__ import annotations


def compose_health_endpoint_violations(endpoints: object, *, maximum_timeout_seconds: int = 30) -> tuple[str, ...]:
    if not isinstance(maximum_timeout_seconds, int) or isinstance(maximum_timeout_seconds, bool) or maximum_timeout_seconds < 1: raise ValueError('maximum_timeout_seconds must be positive')
    if not isinstance(endpoints, list) or not endpoints: return ('health_endpoints_must_be_a_non_empty_list',)
    violations: list[str] = []; seen: set[str] = set()
    for position, endpoint in enumerate(endpoints):
        prefix = f'endpoint_{position}'
        if not isinstance(endpoint, dict): violations.append(f'{prefix}:endpoint_must_be_an_object'); continue
        service = endpoint.get('service')
        if not isinstance(service, str) or not service.strip(): violations.append(f'{prefix}:service_is_required')
        elif service in seen: violations.append(f'{prefix}:service_must_be_unique')
        else: seen.add(service)
        path = endpoint.get('path')
        if not isinstance(path, str) or not path.startswith('/') or '?' in path or '#' in path: violations.append(f'{prefix}:path_must_be_an_absolute_endpoint')
        if endpoint.get('expected_status') != 200: violations.append(f'{prefix}:expected_status_must_be_200')
        timeout = endpoint.get('timeout_seconds')
        if not isinstance(timeout, int) or isinstance(timeout, bool) or not 0 < timeout <= maximum_timeout_seconds: violations.append(f'{prefix}:timeout_must_be_within_budget')
        if endpoint.get('authentication_required') is not False: violations.append(f'{prefix}:health_probe_must_not_require_authentication')
    return tuple(violations)
