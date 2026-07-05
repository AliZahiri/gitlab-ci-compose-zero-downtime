from __future__ import annotations


def smoke_manifest_warnings(checks: list[dict[str, object]]) -> tuple[str, ...]:
    warnings: list[str] = []
    if not checks:
        return ("smoke_checks_missing",)
    for index, check in enumerate(checks):
        prefix = f"check_{index}"
        if not check.get("name"):
            warnings.append(f"{prefix}_name_missing")
        if not check.get("path"):
            warnings.append(f"{prefix}_path_missing")
        timeout = check.get("timeout_seconds")
        if not isinstance(timeout, (int, float)) or timeout <= 0:
            warnings.append(f"{prefix}_timeout_must_be_positive")
    return tuple(warnings)


def smoke_manifest_is_ready(checks: list[dict[str, object]]) -> bool:
    return not smoke_manifest_warnings(checks)
