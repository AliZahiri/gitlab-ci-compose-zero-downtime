from __future__ import annotations

import re

from compose_zero_downtime.transition_journal import transition_journal_violations


_DIGEST = re.compile(r"sha256:[0-9a-f]{64}\Z")


def promotion_resume_violations(checkpoint: dict[str, object]) -> tuple[str, ...]:
    violations: list[str] = []
    release_id = checkpoint.get("release_id")
    if not isinstance(release_id, str) or not release_id.strip():
        violations.append("release_id_is_required")
    current = checkpoint.get("current_color")
    candidate = checkpoint.get("candidate_color")
    if current not in {"blue", "green"} or candidate not in {"blue", "green"}:
        violations.append("deployment_colors_must_be_blue_or_green")
    elif current == candidate:
        violations.append("candidate_color_must_differ_from_current_color")
    digest = checkpoint.get("candidate_digest")
    if not isinstance(digest, str) or not _DIGEST.fullmatch(digest):
        violations.append("candidate_digest_must_be_immutable")
    states = checkpoint.get("states")
    if not isinstance(states, (list, tuple)):
        violations.append("transition_journal_is_required")
    else:
        violations.extend(f"journal:{item}" for item in transition_journal_violations(states))
    if checkpoint.get("rollback_ready") is not True:
        violations.append("rollback_readiness_must_be_confirmed")
    return tuple(violations)


def promotion_can_resume(checkpoint: dict[str, object]) -> bool:
    return not promotion_resume_violations(checkpoint)


def promotion_resume_report(checkpoint: dict[str, object]) -> dict[str, object]:
    violations = promotion_resume_violations(checkpoint)
    states = checkpoint.get("states")
    return {
        "resume_allowed": not violations,
        "release_id": checkpoint.get("release_id"),
        "current_color": checkpoint.get("current_color"),
        "candidate_color": checkpoint.get("candidate_color"),
        "journal_state_count": len(states) if isinstance(states, (list, tuple)) else 0,
        "violations": list(violations),
    }
