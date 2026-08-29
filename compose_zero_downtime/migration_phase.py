from __future__ import annotations


_ALLOWED_PHASES = {"expand", "backfill", "contract"}
_ALLOWED_STATUSES = {"pending", "running", "succeeded"}


def migration_phase_violations(evidence: dict[str, object]) -> tuple[str, ...]:
    violations: list[str] = []
    for field in ("release_id", "schema_version", "migration_checksum"):
        if not isinstance(evidence.get(field), str) or not evidence[field].strip():
            violations.append(f"{field}_is_required")
    phases = evidence.get("phases")
    if not isinstance(phases, list) or not phases:
        return tuple([*violations, "migration_phase_evidence_is_required"])
    observed: dict[str, str] = {}
    for index, phase in enumerate(phases):
        if not isinstance(phase, dict):
            violations.append(f"phase_{index}:must_be_an_object")
            continue
        name, status = phase.get("name"), phase.get("status")
        if name not in _ALLOWED_PHASES:
            violations.append(f"phase_{index}:name_is_invalid")
        elif name in observed:
            violations.append(f"phase_{index}:name_must_be_unique")
        else:
            observed[name] = status if isinstance(status, str) else ""
        if status not in _ALLOWED_STATUSES:
            violations.append(f"phase_{index}:status_is_invalid")
    if observed.get("expand") != "succeeded":
        violations.append("expand_phase_must_succeed_before_promotion")
    if evidence.get("backward_compatible") is not True:
        violations.append("expanded_schema_must_be_backward_compatible")
    old_color_rollback_eligible = evidence.get("old_color_rollback_eligible")
    if not isinstance(old_color_rollback_eligible, bool):
        violations.append("old_color_rollback_eligible_must_be_boolean")
    elif old_color_rollback_eligible and observed.get("contract") == "succeeded":
        violations.append("contract_phase_must_wait_until_rollback_window_closes")
    return tuple(violations)


def migration_phase_is_safe_for_promotion(evidence: dict[str, object]) -> bool:
    return not migration_phase_violations(evidence)
