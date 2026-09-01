from __future__ import annotations


def credential_redaction_violations(evidence: dict[str, object], *, required_categories: frozenset[str] = frozenset({"token", "password", "authorization", "private_key"})) -> tuple[str, ...]:
    violations: list[str] = []
    for field in ("artifact_id", "scanner_version"):
        if not isinstance(evidence.get(field), str) or not evidence[field].strip():
            violations.append(f"{field}_is_required")
    if evidence.get("scan_completed") is not True:
        violations.append("credential_scan_must_complete")
    categories = evidence.get("covered_categories")
    if not isinstance(categories, list) or any(not isinstance(item, str) for item in categories):
        violations.append("covered_categories_must_be_a_string_list")
    else:
        missing = required_categories.difference(categories)
        if missing:
            violations.append("required_sensitive_categories_are_not_covered")
    exposed = evidence.get("exposed_finding_ids")
    if not isinstance(exposed, list):
        violations.append("exposed_finding_ids_must_be_a_list")
    elif exposed:
        violations.append("unredacted_credentials_detected")
    return tuple(violations)


def deployment_artifact_is_redacted(evidence: dict[str, object], **policy: object) -> bool:
    return not credential_redaction_violations(evidence, **policy)
