from __future__ import annotations


def _target_component(value: object, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"target {name} must be a non-empty string")
    return value.strip().lower()


def release_platform_compatibility_violations(artifacts: dict[str, object], *, target_os: str, target_architecture: str) -> tuple[str, ...]:
    expected_os = _target_component(target_os, "operating system")
    expected_architecture = _target_component(target_architecture, "architecture")
    violations: list[str] = []
    for role in ("candidate", "rollback"):
        artifact = artifacts.get(role)
        if not isinstance(artifact, dict):
            violations.append(f"artifact:{role}:platform_evidence_is_required")
            continue
        if not str(artifact.get("image", "")).strip():
            violations.append(f"artifact:{role}:image_is_required")
        observed_os = artifact.get("os")
        if not isinstance(observed_os, str) or observed_os.strip().lower() != expected_os:
            violations.append(f"artifact:{role}:os_must_match_target")
        observed_architecture = artifact.get("architecture")
        if not isinstance(observed_architecture, str) or observed_architecture.strip().lower() != expected_architecture:
            violations.append(f"artifact:{role}:architecture_must_match_target")
    return tuple(violations)


def release_platform_is_compatible(artifacts: dict[str, object], **target: object) -> bool:
    return not release_platform_compatibility_violations(artifacts, **target)
