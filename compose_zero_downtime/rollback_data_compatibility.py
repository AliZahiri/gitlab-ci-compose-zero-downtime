from __future__ import annotations

import re


_DIGEST = re.compile(r"sha256:[0-9a-f]{64}\Z")


def rollback_data_compatibility_violations(evidence: dict[str, object]) -> tuple[str, ...]:
    violations: list[str] = []
    if not isinstance(evidence.get("rollback_image_digest"), str) or not _DIGEST.fullmatch(evidence["rollback_image_digest"]):
        violations.append("rollback_image_digest_is_invalid")
    current = evidence.get("current_schema_version")
    minimum = evidence.get("rollback_min_schema_version")
    maximum = evidence.get("rollback_max_schema_version")
    versions = (current, minimum, maximum)
    if any(not isinstance(value, int) or isinstance(value, bool) or value < 0 for value in versions):
        violations.append("schema_versions_must_be_non_negative_integers")
    elif not minimum <= current <= maximum:
        violations.append("current_schema_is_not_supported_by_rollback_target")
    if evidence.get("migration_reversible") is not True and evidence.get("rollback_forward_compatible") is not True:
        violations.append("migration_requires_reversibility_or_forward_compatibility")
    if evidence.get("backup_verified") is not True:
        violations.append("verified_backup_is_required_before_rollback")
    return tuple(violations)


def rollback_data_is_compatible(evidence: dict[str, object]) -> bool:
    return not rollback_data_compatibility_violations(evidence)
