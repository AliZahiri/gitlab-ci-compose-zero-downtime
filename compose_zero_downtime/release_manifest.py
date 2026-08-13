from __future__ import annotations

import re
from datetime import datetime


_DIGEST = re.compile(r"sha256:[0-9a-f]{64}\Z")
_SHA = re.compile(r"[0-9a-f]{40}\Z")


def _timestamp(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None and parsed.utcoffset() is not None else None


def release_manifest_violations(manifest: dict[str, object]) -> tuple[str, ...]:
    violations: list[str] = []
    if not isinstance(manifest.get("release_id"), str) or not manifest["release_id"].strip():
        violations.append("release_id_is_required")
    if not isinstance(manifest.get("image_digest"), str) or not _DIGEST.fullmatch(manifest["image_digest"]):
        violations.append("image_digest_must_be_immutable")
    if not isinstance(manifest.get("source_revision"), str) or not _SHA.fullmatch(manifest["source_revision"]):
        violations.append("source_revision_must_be_full_sha")
    if not isinstance(manifest.get("config_sha256"), str) or not re.fullmatch(r"[0-9a-f]{64}", manifest["config_sha256"]):
        violations.append("config_sha256_is_invalid")
    if _timestamp(manifest.get("created_at")) is None:
        violations.append("created_at_must_be_timezone_aware")
    return tuple(violations)


def release_manifest_is_complete(manifest: dict[str, object]) -> bool:
    return not release_manifest_violations(manifest)
