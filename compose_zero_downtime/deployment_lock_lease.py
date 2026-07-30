from __future__ import annotations

from datetime import datetime
import re


_LEASE_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:-]{7,127}\Z")


def _timestamp(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None and parsed.utcoffset() is not None else None


def deployment_lock_lease_violations(lease: dict[str, object], *, now: datetime, maximum_duration_seconds: int = 1800, minimum_remaining_seconds: int = 120) -> tuple[str, ...]:
    if maximum_duration_seconds <= 0 or minimum_remaining_seconds < 0 or minimum_remaining_seconds > maximum_duration_seconds:
        raise ValueError("lease duration policy is invalid")
    violations: list[str] = []
    if not isinstance(lease.get("lease_id"), str) or not _LEASE_ID.fullmatch(lease["lease_id"]):
        violations.append("lease_id_is_invalid")
    if not str(lease.get("holder", "")).strip():
        violations.append("lease_holder_is_required")
    acquired = _timestamp(lease.get("acquired_at"))
    expires = _timestamp(lease.get("expires_at"))
    if acquired is None:
        violations.append("acquired_at_must_be_timezone_aware")
    if expires is None:
        violations.append("expires_at_must_be_timezone_aware")
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("current time must be timezone-aware")
    if acquired is not None and expires is not None:
        duration = (expires - acquired).total_seconds()
        if duration <= 0:
            violations.append("lease_expiry_must_follow_acquisition")
        elif duration > maximum_duration_seconds:
            violations.append("lease_duration_exceeds_maximum")
        remaining = (expires - now).total_seconds()
        if remaining < minimum_remaining_seconds:
            violations.append("lease_remaining_time_is_insufficient")
        if acquired > now:
            violations.append("lease_acquisition_is_in_the_future")
    return tuple(violations)


def deployment_lock_lease_is_usable(lease: dict[str, object], **policy: object) -> bool:
    return not deployment_lock_lease_violations(lease, **policy)
