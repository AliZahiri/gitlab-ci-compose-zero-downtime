from __future__ import annotations

import re


_SENSITIVE_NAME = re.compile(r"(?:^|_)(?:password|secret|token|api_key|private_key)(?:_|$)", re.IGNORECASE)
_VARIABLE_REFERENCE = re.compile(r"\$\{[A-Z][A-Z0-9_]*\}\Z")


def compose_secret_reference_violations(services: dict[str, object], *, secret_mount_root: str = "/run/secrets") -> tuple[str, ...]:
    if not isinstance(secret_mount_root, str) or not secret_mount_root.startswith("/") or secret_mount_root.rstrip("/") != secret_mount_root:
        raise ValueError("secret mount root must be an absolute path without a trailing slash")
    if not isinstance(services, dict) or not services:
        return ("at_least_one_service_is_required",)

    violations: list[str] = []
    for raw_name, service in services.items():
        name = raw_name.strip() if isinstance(raw_name, str) else ""
        if not name:
            violations.append("service_name_is_required")
            continue
        if not isinstance(service, dict):
            violations.append(f"service:{name}:metadata_is_required")
            continue
        environment = service.get("environment", {})
        if not isinstance(environment, dict):
            violations.append(f"service:{name}:environment_must_be_a_mapping")
            continue
        for raw_key, value in environment.items():
            key = raw_key.strip() if isinstance(raw_key, str) else ""
            if not key:
                violations.append(f"service:{name}:environment_key_is_required")
                continue
            base_name = key.removesuffix("_FILE")
            if not _SENSITIVE_NAME.search(base_name):
                continue
            if key.endswith("_FILE"):
                expected_prefix = secret_mount_root + "/"
                if not isinstance(value, str) or not value.startswith(expected_prefix) or ".." in value.split("/"):
                    violations.append(f"service:{name}:environment:{key}:must_reference_secret_mount")
            elif not isinstance(value, str) or not _VARIABLE_REFERENCE.fullmatch(value):
                violations.append(f"service:{name}:environment:{key}:must_not_embed_sensitive_value")
    return tuple(violations)


def compose_secret_references_are_safe(services: dict[str, object], **policy: object) -> bool:
    return not compose_secret_reference_violations(services, **policy)
