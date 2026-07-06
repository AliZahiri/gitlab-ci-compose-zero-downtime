from __future__ import annotations


def traffic_shift_warnings(steps: list[dict[str, int]]) -> tuple[str, ...]:
    if not steps:
        return ("traffic_shift_steps_missing",)
    warnings: list[str] = []
    percentages = [step.get("percent") for step in steps]
    if percentages[0] != 0:
        warnings.append("traffic_shift_must_start_at_zero")
    if percentages[-1] != 100:
        warnings.append("traffic_shift_must_end_at_full")
    if any(not isinstance(value, int) or value < 0 or value > 100 for value in percentages):
        warnings.append("traffic_shift_percent_must_be_between_0_and_100")
    if percentages != sorted(percentages):
        warnings.append("traffic_shift_percentages_must_be_ordered")
    if any(not isinstance(step.get("observe_seconds"), int) or step["observe_seconds"] <= 0 for step in steps):
        warnings.append("observe_seconds_must_be_positive")
    return tuple(warnings)


def traffic_shift_plan_is_safe(steps: list[dict[str, int]]) -> bool:
    return not traffic_shift_warnings(steps)
