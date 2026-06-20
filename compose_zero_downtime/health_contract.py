from __future__ import annotations

REQUIRED_READINESS_CHECKS = (
    "http_accepting_requests",
    "critical_dependencies_reachable",
    "required_migrations_applied",
    "minimal_real_request_served",
)


def missing_readiness_checks(checks: list[str] | tuple[str, ...] | set[str]) -> tuple[str, ...]:
    provided = set(checks)
    return tuple(check for check in REQUIRED_READINESS_CHECKS if check not in provided)


def readiness_contract_is_satisfied(checks: list[str] | tuple[str, ...] | set[str]) -> bool:
    return not missing_readiness_checks(checks)
