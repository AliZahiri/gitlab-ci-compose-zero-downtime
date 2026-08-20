from __future__ import annotations

from datetime import datetime
import re


_DIGEST = re.compile(r"sha256:[0-9a-f]{64}\Z")
_TICKET = re.compile(r"[A-Z][A-Z0-9]+-\d+\Z")


def promotion_approval_violations(evidence: dict[str, object]) -> tuple[str, ...]:
    violations: list[str] = []
    if not isinstance(evidence.get("release_id"), str) or not evidence["release_id"].strip():
        violations.append("release_id_is_required")
    digest = evidence.get("candidate_digest")
    if not isinstance(digest, str) or not _DIGEST.fullmatch(digest):
        violations.append("candidate_digest_must_be_immutable")
    ticket = evidence.get("change_ticket")
    if not isinstance(ticket, str) or not _TICKET.fullmatch(ticket):
        violations.append("change_ticket_is_invalid")
    if not isinstance(evidence.get("approved_by"), str) or not evidence["approved_by"].strip():
        violations.append("approved_by_is_required")
    if _parse_timestamp(evidence.get("approved_at")) is None:
        violations.append("approved_at_must_be_timezone_aware")
    if evidence.get("change_window_open") is not True:
        violations.append("change_window_must_be_open")
    if evidence.get("rollback_ready") is not True:
        violations.append("rollback_must_be_ready")
    return tuple(violations)


def promotion_is_approved(evidence: dict[str, object]) -> bool:
    return not promotion_approval_violations(evidence)


def _parse_timestamp(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None and parsed.utcoffset() is not None else None
