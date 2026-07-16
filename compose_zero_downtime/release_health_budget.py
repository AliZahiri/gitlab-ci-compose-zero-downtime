from __future__ import annotations


def release_health_warnings(summary: dict[str, object], *, max_failures: int = 0, min_successes: int = 1) -> tuple[str, ...]:
    warnings: list[str] = []
    successes = summary.get("successes")
    failures = summary.get("failures")
    if not isinstance(successes, int) or successes < min_successes:
        warnings.append("successful_probes_below_minimum")
    if not isinstance(failures, int) or failures > max_failures:
        warnings.append("failed_probes_exceed_budget")
    return tuple(warnings)


def release_health_is_within_budget(summary: dict[str, object], *, max_failures: int = 0, min_successes: int = 1) -> bool:
    return not release_health_warnings(summary, max_failures=max_failures, min_successes=min_successes)
