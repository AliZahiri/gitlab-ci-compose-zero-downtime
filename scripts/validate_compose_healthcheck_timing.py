from __future__ import annotations


def compose_healthcheck_timing_violations(healthchecks: object, *, maximum_readiness_seconds: int = 300) -> tuple[str, ...]:
    if not isinstance(maximum_readiness_seconds, int) or isinstance(maximum_readiness_seconds, bool) or maximum_readiness_seconds < 1: raise ValueError('maximum_readiness_seconds must be positive')
    if not isinstance(healthchecks, list) or not healthchecks: return ('healthchecks_must_be_a_non_empty_list',)
    violations: list[str] = []
    for position, healthcheck in enumerate(healthchecks):
        prefix = f'healthcheck_{position}'
        if not isinstance(healthcheck, dict): violations.append(f'{prefix}:healthcheck_must_be_an_object'); continue
        values = {name: healthcheck.get(name) for name in ('interval_seconds', 'timeout_seconds', 'retries', 'start_period_seconds')}
        if any(not isinstance(value, int) or isinstance(value, bool) or value < 0 for value in values.values()): violations.append(f'{prefix}:timing_values_must_be_non_negative_integers'); continue
        if values['interval_seconds'] < 1 or values['timeout_seconds'] < 1 or values['retries'] < 1: violations.append(f'{prefix}:interval_timeout_and_retries_must_be_positive')
        elif values['timeout_seconds'] > values['interval_seconds']: violations.append(f'{prefix}:timeout_must_not_exceed_interval')
        elif values['start_period_seconds'] + values['interval_seconds'] * values['retries'] > maximum_readiness_seconds: violations.append(f'{prefix}:worst_case_readiness_exceeds_budget')
    return tuple(violations)
