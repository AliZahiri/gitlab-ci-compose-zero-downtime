from __future__ import annotations

from datetime import datetime


def _timestamp(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None and parsed.utcoffset() is not None else None


def deployment_concurrency_scope_violations(leases: list[dict[str, object]], *, now: datetime, maximum_lease_seconds: int = 1800) -> tuple[str, ...]:
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("current time must be timezone-aware")
    if not isinstance(maximum_lease_seconds, int) or isinstance(maximum_lease_seconds, bool) or maximum_lease_seconds <= 0:
        raise ValueError("maximum lease duration must be positive")
    if not leases:
        return ("at_least_one_deployment_lease_is_required",)
    violations: list[str] = []
    seen_ids, seen_environments, seen_targets = set(), set(), set()
    for index, lease in enumerate(leases):
        for field, seen in (("lease_id", seen_ids), ("environment", seen_environments), ("traffic_target", seen_targets)):
            value = lease.get(field)
            if not isinstance(value, str) or not value.strip():
                violations.append(f"lease_{index}:{field}_is_required")
            elif value in seen:
                violations.append(f"lease_{index}:{field}_must_be_unique")
            seen.add(value)
        expires_at = _timestamp(lease.get("expires_at"))
        if expires_at is None:
            violations.append(f"lease_{index}:expires_at_must_be_timezone_aware")
        else:
            duration = (expires_at - now).total_seconds()
            if not 0 < duration <= maximum_lease_seconds:
                violations.append(f"lease_{index}:expiry_must_be_within_lease_budget")
    return tuple(violations)


def deployment_concurrency_scope_is_safe(leases: list[dict[str, object]], **policy: object) -> bool:
    return not deployment_concurrency_scope_violations(leases, **policy)
