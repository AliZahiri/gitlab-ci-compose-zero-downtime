from __future__ import annotations


def deploy_lock_warnings(lock: dict[str, object]) -> tuple[str, ...]:
    warnings: list[str] = []
    if not lock.get("name"):
        warnings.append("lock_name_missing")
    if not lock.get("owner"):
        warnings.append("lock_owner_missing")
    ttl = lock.get("ttl_seconds")
    if not isinstance(ttl, int) or ttl <= 0:
        warnings.append("ttl_seconds_must_be_positive")
    return tuple(warnings)


def deploy_lock_is_valid(lock: dict[str, object]) -> bool:
    return not deploy_lock_warnings(lock)
