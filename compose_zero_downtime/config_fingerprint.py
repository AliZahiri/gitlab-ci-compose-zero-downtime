from __future__ import annotations

import re


_SHA256 = re.compile(r"[0-9a-f]{64}\Z")


def config_fingerprint_violations(evidence: dict[str, dict[str, object]], *, required_components: tuple[str, ...] = ("compose", "proxy", "environment")) -> tuple[str, ...]:
    if not required_components or any(not str(item).strip() for item in required_components) or len(set(required_components)) != len(required_components):
        raise ValueError("required components must be unique and non-empty")
    violations: list[str] = []
    for component in required_components:
        item = evidence.get(component)
        if not isinstance(item, dict):
            violations.append(f"component:{component}:fingerprint_evidence_is_required")
            continue
        planned = item.get("planned_sha256")
        observed = item.get("observed_sha256")
        rollback = item.get("rollback_sha256")
        if not isinstance(planned, str) or not _SHA256.fullmatch(planned):
            violations.append(f"component:{component}:planned_fingerprint_is_invalid")
        if not isinstance(observed, str) or not _SHA256.fullmatch(observed):
            violations.append(f"component:{component}:observed_fingerprint_is_invalid")
        if isinstance(planned, str) and isinstance(observed, str) and _SHA256.fullmatch(planned) and _SHA256.fullmatch(observed) and planned != observed:
            violations.append(f"component:{component}:planned_and_observed_fingerprints_differ")
        if not isinstance(rollback, str) or not _SHA256.fullmatch(rollback):
            violations.append(f"component:{component}:rollback_fingerprint_is_invalid")
    return tuple(violations)


def release_config_is_pinned(evidence: dict[str, dict[str, object]], **policy: object) -> bool:
    return not config_fingerprint_violations(evidence, **policy)
