from __future__ import annotations


def upstream_target_parity_violations(*, expected_targets: tuple[str, ...], rendered_targets: list[str], nginx_config_valid: bool) -> tuple[str, ...]:
    expected = tuple(value.strip() for value in expected_targets)
    rendered = [value.strip() if isinstance(value, str) else "" for value in rendered_targets]
    if not expected or any(not value for value in expected) or len(set(expected)) != len(expected):
        raise ValueError("expected targets must be unique and non-empty")
    violations: list[str] = []
    if nginx_config_valid is not True:
        violations.append("nginx_configuration_must_be_valid")
    if any(not value for value in rendered):
        violations.append("rendered_targets_must_be_non_empty_strings")
    if len(rendered) != len(set(rendered)):
        violations.append("rendered_targets_must_be_unique")
    missing = sorted(set(expected) - set(rendered))
    unexpected = sorted(set(rendered) - set(expected))
    if missing:
        violations.append("expected_upstream_target_is_missing")
    if unexpected:
        violations.append("unexpected_upstream_target_is_rendered")
    return tuple(violations)


def nginx_upstreams_match_plan(**evidence: object) -> bool:
    return not upstream_target_parity_violations(**evidence)
