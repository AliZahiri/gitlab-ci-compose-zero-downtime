from __future__ import annotations

from datetime import datetime
import re

_SHA256 = re.compile(r"sha256:[0-9a-f]{64}\Z")


def sbom_attestation_violations(attestation: dict[str, object], *, release_digest: str) -> tuple[str, ...]:
    violations: list[str] = []
    if not _SHA256.fullmatch(release_digest):
        raise ValueError("release_digest must be a sha256 digest")
    if attestation.get("subject_digest") != release_digest:
        violations.append("sbom_subject_must_match_release_digest")
    if not isinstance(attestation.get("sbom_digest"), str) or not _SHA256.fullmatch(attestation["sbom_digest"]):
        violations.append("sbom_digest_is_invalid")
    if attestation.get("format") not in {"CycloneDX", "SPDX"}:
        violations.append("sbom_format_is_unsupported")
    if attestation.get("signature_verified") is not True:
        violations.append("sbom_signature_must_be_verified")
    if _timestamp(attestation.get("generated_at")) is None:
        violations.append("generated_at_must_be_timezone_aware")
    return tuple(violations)


def sbom_attestation_is_valid(attestation: dict[str, object], *, release_digest: str) -> bool:
    return not sbom_attestation_violations(attestation, release_digest=release_digest)


def _timestamp(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None and parsed.utcoffset() is not None else None
