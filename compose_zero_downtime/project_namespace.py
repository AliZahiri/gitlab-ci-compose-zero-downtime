from __future__ import annotations

import re


_SLUG = re.compile(r"[a-z0-9][a-z0-9-]{0,30}\Z")


def expected_project_name(stack: str, environment: str) -> str:
    if not _SLUG.fullmatch(stack) or not _SLUG.fullmatch(environment):
        raise ValueError("stack and environment must be lowercase slugs")
    return f"{stack}-{environment}"


def project_namespace_violations(evidence: dict[str, object]) -> tuple[str, ...]:
    violations: list[str] = []
    try:
        expected = expected_project_name(str(evidence.get("stack", "")), str(evidence.get("environment", "")))
    except ValueError:
        return ("stack_and_environment_must_be_lowercase_slugs",)
    if evidence.get("project_name") != expected:
        violations.append("project_name_must_match_stack_and_environment")
    resources = evidence.get("resources")
    if not isinstance(resources, list) or not resources:
        return tuple([*violations, "at_least_one_runtime_resource_is_required"])
    seen: set[tuple[str, str]] = set()
    prefix = expected + "_"
    for index, resource in enumerate(resources):
        if not isinstance(resource, dict):
            violations.append(f"resource_{index}:must_be_an_object")
            continue
        kind, name = resource.get("kind"), resource.get("name")
        if kind not in {"container", "network", "volume"}:
            violations.append(f"resource_{index}:kind_is_invalid")
        if not isinstance(name, str) or not name.strip():
            violations.append(f"resource_{index}:name_is_required")
            continue
        identity = (str(kind), name)
        if identity in seen:
            violations.append(f"resource_{index}:identity_must_be_unique")
        seen.add(identity)
        if resource.get("shared") is True:
            if resource.get("shared_resource_approved") is not True:
                violations.append(f"resource_{index}:shared_resource_requires_approval")
        elif not name.startswith(prefix):
            violations.append(f"resource_{index}:name_must_use_project_namespace")
    return tuple(violations)


def project_namespace_is_isolated(evidence: dict[str, object]) -> bool:
    return not project_namespace_violations(evidence)
