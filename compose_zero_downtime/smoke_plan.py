from __future__ import annotations

REQUIRED_SMOKE_CHECKS = (
    "public_endpoint_success",
    "expected_version_or_color",
    "critical_api_route",
    "stable_error_rate",
)


def missing_smoke_checks(checks: list[str] | tuple[str, ...] | set[str]) -> tuple[str, ...]:
    present = set(checks)
    return tuple(check for check in REQUIRED_SMOKE_CHECKS if check not in present)


def smoke_plan_warnings(
    checks: list[str] | tuple[str, ...] | set[str],
    *,
    timeout_seconds: float = 5.0,
    max_timeout_seconds: float = 15.0,
) -> tuple[str, ...]:
    warnings = list(missing_smoke_checks(checks))
    if timeout_seconds <= 0:
        warnings.append("timeout_seconds_must_be_positive")
    if timeout_seconds > max_timeout_seconds:
        warnings.append("timeout_seconds_exceeds_release_budget")
    return tuple(warnings)


def smoke_plan_is_complete(
    checks: list[str] | tuple[str, ...] | set[str],
    *,
    timeout_seconds: float = 5.0,
) -> bool:
    return not smoke_plan_warnings(checks, timeout_seconds=timeout_seconds)
