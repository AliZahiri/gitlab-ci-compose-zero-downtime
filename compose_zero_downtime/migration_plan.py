from __future__ import annotations


ALLOWED_PHASES = ("expand", "backfill", "contract")


def migration_plan_warnings(steps: list[dict[str, object]]) -> tuple[str, ...]:
    if not steps:
        return ("migration_plan_is_empty",)
    warnings: list[str] = []
    phases: list[str] = []
    for index, step in enumerate(steps):
        phase = str(step.get("phase", "")).strip().lower()
        phases.append(phase)
        if phase not in ALLOWED_PHASES:
            warnings.append(f"step_{index}_phase_is_invalid")
        if phase == "contract":
            if step.get("compatibility_window_complete") is not True:
                warnings.append(f"step_{index}_compatibility_window_incomplete")
            if step.get("rollback_tested") is not True:
                warnings.append(f"step_{index}_rollback_not_tested")
    if "contract" in phases and ("expand" not in phases or phases.index("expand") > phases.index("contract")):
        warnings.append("expand_must_precede_contract")
    return tuple(warnings)


def migration_plan_is_safe(steps: list[dict[str, object]]) -> bool:
    return not migration_plan_warnings(steps)
