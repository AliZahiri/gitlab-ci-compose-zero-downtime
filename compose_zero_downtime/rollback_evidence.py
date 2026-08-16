from __future__ import annotations

from datetime import datetime
import re


_DIGEST = re.compile(r"sha256:[0-9a-f]{64}\Z")


def rollback_evidence_violations(record: dict[str, object]) -> tuple[str, ...]:
    violations: list[str] = []
    if record.get("active_color") not in {"blue", "green"}:
        violations.append("active_color_must_be_blue_or_green")
    if not isinstance(record.get("rollback_image_digest"), str) or not _DIGEST.fullmatch(record["rollback_image_digest"]):
        violations.append("rollback_image_digest_must_be_immutable")
    value = record.get("decision_at")
    try:
        decided_at = datetime.fromisoformat(value.replace("Z", "+00:00")) if isinstance(value, str) else None
    except ValueError:
        decided_at = None
    if decided_at is None or decided_at.tzinfo is None or decided_at.utcoffset() is None:
        violations.append("decision_at_must_be_timezone_aware")
    if not isinstance(record.get("health_reason"), str) or not record["health_reason"].strip():
        violations.append("health_reason_is_required")
    return tuple(violations)


def rollback_evidence_is_actionable(record: dict[str, object]) -> bool:
    return not rollback_evidence_violations(record)
