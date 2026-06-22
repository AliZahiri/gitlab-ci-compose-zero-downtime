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


def smoke_plan_is_complete(checks: list[str] | tuple[str, ...] | set[str]) -> bool:
    return not missing_smoke_checks(checks)
