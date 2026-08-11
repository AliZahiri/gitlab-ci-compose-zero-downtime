from __future__ import annotations

import re
from datetime import datetime


_DIGEST = re.compile(r"sha256:[0-9a-f]{64}\Z")


def _timestamp(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None and parsed.utcoffset() is not None else None


def image_signature_evidence_violations(evidence: dict[str, object], *, trusted_signers: set[str]) -> tuple[str, ...]:
    if not trusted_signers:
        raise ValueError("at least one trusted signer is required")
    violations: list[str] = []
    if not isinstance(evidence.get("image_digest"), str) or not _DIGEST.fullmatch(evidence["image_digest"]):
        violations.append("image_digest_must_be_immutable")
    if evidence.get("signer") not in trusted_signers:
        violations.append("signer_must_be_trusted")
    if evidence.get("signature_verified") is not True:
        violations.append("signature_must_be_verified")
    if _timestamp(evidence.get("verified_at")) is None:
        violations.append("verified_at_must_be_timezone_aware")
    return tuple(violations)


def image_signature_evidence_is_safe(evidence: dict[str, object], *, trusted_signers: set[str]) -> bool:
    return not image_signature_evidence_violations(evidence, trusted_signers=trusted_signers)
