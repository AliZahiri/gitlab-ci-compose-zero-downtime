from __future__ import annotations

_ALLOWED_STRATEGIES = frozenset({"expand-contract", "backward-compatible"})


def migration_compatibility_violations(evidence: dict[str, object]) -> tuple[str, ...]:
    violations: list[str] = []
    if not isinstance(evidence.get("migration_id"), str) or not evidence["migration_id"].strip():
        violations.append("migration_id_is_required")
    if evidence.get("strategy") not in _ALLOWED_STRATEGIES:
        violations.append("strategy_must_be_compatible")
    if evidence.get("backward_compatibility_checked") is not True:
        violations.append("backward_compatibility_check_must_pass")
    if evidence.get("rollback_tested") is not True:
        violations.append("rollback_test_must_pass")
    return tuple(violations)


def migration_is_safe_to_promote(evidence: dict[str, object]) -> bool:
    return not migration_compatibility_violations(evidence)
