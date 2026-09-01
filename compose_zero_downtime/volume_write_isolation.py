from __future__ import annotations


def volume_write_isolation_violations(active: list[dict[str, object]], candidate: list[dict[str, object]]) -> tuple[str, ...]:
    violations: list[str] = []
    normalized: dict[str, dict[str, bool]] = {}
    for color, mounts in (("active", active), ("candidate", candidate)):
        if not isinstance(mounts, list):
            violations.append(f"{color}:mounts_must_be_a_list")
            continue
        targets: set[str] = set()
        sources: dict[str, bool] = {}
        for index, mount in enumerate(mounts):
            if not isinstance(mount, dict):
                violations.append(f"{color}:mount_{index}_must_be_an_object")
                continue
            source = mount.get("source")
            target = mount.get("target")
            read_only = mount.get("read_only")
            if not isinstance(source, str) or not source.strip():
                violations.append(f"{color}:mount_{index}_source_is_required")
            if not isinstance(target, str) or not target.startswith("/"):
                violations.append(f"{color}:mount_{index}_target_must_be_absolute")
            elif target in targets:
                violations.append(f"{color}:mount_targets_must_be_unique")
            else:
                targets.add(target)
            if not isinstance(read_only, bool):
                violations.append(f"{color}:mount_{index}_read_only_must_be_boolean")
            if isinstance(source, str) and source.strip() and isinstance(read_only, bool):
                sources[source] = read_only
        normalized[color] = sources
    for source in set(normalized.get("active", {})).intersection(normalized.get("candidate", {})):
        if not normalized["active"][source] or not normalized["candidate"][source]:
            violations.append(f"shared_writable_volume:{source}")
    return tuple(violations)


def volumes_are_write_isolated(active: list[dict[str, object]], candidate: list[dict[str, object]]) -> bool:
    return not volume_write_isolation_violations(active, candidate)
