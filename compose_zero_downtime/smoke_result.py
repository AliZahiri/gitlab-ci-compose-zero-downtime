from __future__ import annotations


def smoke_result_passed(result: dict[str, object], *, max_duration_ms: int = 2000) -> bool:
    status = result.get("status_code")
    duration = result.get("duration_ms")
    return isinstance(status, int) and 200 <= status < 400 and isinstance(duration, (int, float)) and duration <= max_duration_ms


def summarize_smoke_result(result: dict[str, object], *, max_duration_ms: int = 2000) -> dict[str, object]:
    return {
        "name": str(result.get("name", "smoke")),
        "target": str(result.get("target", "")),
        "passed": smoke_result_passed(result, max_duration_ms=max_duration_ms),
        "status_code": result.get("status_code"),
        "duration_ms": result.get("duration_ms"),
    }
