from __future__ import annotations


def compose_health_response_violations(contracts: object) -> tuple[str, ...]:
    if not isinstance(contracts, list) or not contracts: return ('health_response_contracts_must_be_a_non_empty_list',)
    violations: list[str] = []; services: set[str] = set()
    for position, contract in enumerate(contracts):
        prefix=f'contract_{position}'
        if not isinstance(contract, dict): violations.append(f'{prefix}:contract_must_be_an_object'); continue
        service=contract.get('service')
        if not isinstance(service, str) or not service.strip(): violations.append(f'{prefix}:service_is_required')
        elif service in services: violations.append(f'{prefix}:service_must_be_unique')
        else: services.add(service)
        if contract.get('expected_status') != 200: violations.append(f'{prefix}:expected_status_must_be_200')
        if contract.get('content_type') != 'application/json': violations.append(f'{prefix}:content_type_must_be_json')
        field=contract.get('required_field')
        if not isinstance(field, str) or not field.strip() or '.' in field: violations.append(f'{prefix}:required_field_is_invalid')
    return tuple(violations)
