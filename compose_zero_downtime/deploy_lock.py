from __future__ import annotations


def deploy_lock_warnings(lock: dict[str, object]) -> tuple[str, ...]:
    warnings: list[str] = []
    if not lock.get("name"):
        warnings.append("lock_name_missing")
    if not lock.get("owner"):
        warnings.append("lock_owner_missing")
    if lock.get("release_on_failure") is not True:
        warnings.append("release_on_failure_must_be_enabled")
    ttl = lock.get("ttl_seconds")
    if not isinstance(ttl, int) or ttl <= 0:
        warnings.append("ttl_seconds_must_be_positive")
    elif ttl > 3600:
        warnings.append("ttl_seconds_exceeds_recovery_window")
    return tuple(warnings)


def deploy_lock_is_valid(lock: dict[str, object]) -> bool:
    return not deploy_lock_warnings(lock)
