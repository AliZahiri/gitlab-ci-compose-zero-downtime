from __future__ import annotations

import re


DIGEST_PATTERN = re.compile(r"sha256:[0-9a-f]{64}")


def rollback_artifact_warnings(state: dict[str, object]) -> tuple[str, ...]:
    warnings: list[str] = []
    previous = str(state.get("previous_digest", "")).strip()
    candidate = str(state.get("candidate_digest", "")).strip()
    available = state.get("available_digests")
    verified = state.get("verified_digests")
    if not DIGEST_PATTERN.fullmatch(previous):
        warnings.append("previous_digest_is_not_immutable")
    if previous and previous == candidate:
        warnings.append("previous_digest_matches_candidate")
    if not isinstance(available, list) or previous not in available:
        warnings.append("previous_artifact_is_unavailable")
    if not isinstance(verified, list) or previous not in verified:
        warnings.append("previous_artifact_is_unverified")
    return tuple(warnings)


def rollback_artifact_is_ready(state: dict[str, object]) -> bool:
    return not rollback_artifact_warnings(state)
