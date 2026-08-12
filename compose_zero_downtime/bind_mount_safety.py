from __future__ import annotations


_DANGEROUS_SOURCES = {"/", "/dev", "/proc", "/sys", "/var/run/docker.sock"}


def _valid_root(value: object) -> bool:
    return isinstance(value, str) and value.startswith("/") and value.rstrip("/") == value and value not in {"", "/"}


def _under_root(path: str, roots: tuple[str, ...]) -> bool:
    return any(path == root or path.startswith(root + "/") for root in roots)


def compose_bind_mount_violations(services: dict[str, object], *, allowed_source_roots: tuple[str, ...] = ("/srv/app/config", "/srv/app/data")) -> tuple[str, ...]:
    if not allowed_source_roots or not all(_valid_root(root) for root in allowed_source_roots):
        raise ValueError("allowed source roots must be non-root absolute paths without trailing slashes")
    if not isinstance(services, dict) or not services:
        return ("at_least_one_service_is_required",)

    violations: list[str] = []
    for raw_name, service in services.items():
        name = raw_name.strip() if isinstance(raw_name, str) else ""
        if not name:
            violations.append("service_name_is_required")
            continue
        if not isinstance(service, dict) or not isinstance(service.get("bind_mounts"), list):
            violations.append(f"service:{name}:bind_mounts_must_be_a_list")
            continue
        for index, mount in enumerate(service["bind_mounts"]):
            prefix = f"service:{name}:mount_{index}"
            if not isinstance(mount, dict):
                violations.append(f"{prefix}:metadata_is_required")
                continue
            source = mount.get("source")
            target = mount.get("target")
            if not isinstance(source, str) or not _valid_root(source):
                violations.append(f"{prefix}:source_must_be_an_absolute_non_root_path")
            elif source in _DANGEROUS_SOURCES:
                violations.append(f"{prefix}:source_is_not_permitted")
            elif not _under_root(source, allowed_source_roots):
                violations.append(f"{prefix}:source_must_be_under_an_allowed_root")
            if not isinstance(target, str) or not _valid_root(target):
                violations.append(f"{prefix}:target_must_be_an_absolute_non_root_path")
            if mount.get("read_only") is not True:
                violations.append(f"{prefix}:must_be_read_only")
    return tuple(violations)


def compose_bind_mounts_are_safe(services: dict[str, object], **policy: object) -> bool:
    return not compose_bind_mount_violations(services, **policy)
