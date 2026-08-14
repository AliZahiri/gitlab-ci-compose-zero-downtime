from __future__ import annotations

import re


_DIGEST = re.compile(r"sha256:[0-9a-f]{64}\Z")


def promotion_state_handoff_violations(record: dict[str, object]) -> tuple[str, ...]:
    violations: list[str] = []
    active, standby = record.get("active_color"), record.get("standby_color")
    if active not in {"blue", "green"} or standby not in {"blue", "green"} or active == standby:
        violations.append("active_and_standby_colors_must_be_distinct")
    for field in ("candidate_image_digest", "rollback_image_digest"):
        if not isinstance(record.get(field), str) or not _DIGEST.fullmatch(record[field]):
            violations.append(f"{field}_must_be_immutable")
    if record.get("candidate_healthy") is not True:
        violations.append("candidate_health_must_pass")
    if record.get("rollback_ready") is not True:
        violations.append("rollback_must_be_ready")
    return tuple(violations)


def promotion_state_handoff_is_safe(record: dict[str, object]) -> bool:
    return not promotion_state_handoff_violations(record)
