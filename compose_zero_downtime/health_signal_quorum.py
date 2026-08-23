from __future__ import annotations

from datetime import datetime


def health_signal_quorum_violations(signals: list[object], *, minimum_signals: int = 2, required_consecutive_successes: int = 3) -> tuple[str, ...]:
    if not isinstance(minimum_signals, int) or isinstance(minimum_signals, bool) or minimum_signals < 1:
        raise ValueError("minimum_signals must be positive")
    if not isinstance(required_consecutive_successes, int) or isinstance(required_consecutive_successes, bool) or required_consecutive_successes < 1:
        raise ValueError("required_consecutive_successes must be positive")
    violations: list[str] = []
    seen: set[str] = set()
    for index, signal in enumerate(signals if isinstance(signals, list) else []):
        if not isinstance(signal, dict):
            violations.append(f"signal_{index}:must_be_an_object")
            continue
        probe_id = signal.get("probe_id")
        if not isinstance(probe_id, str) or not probe_id.strip():
            violations.append(f"signal_{index}:probe_id_is_required")
        elif probe_id in seen:
            violations.append(f"signal_{index}:probe_id_must_be_unique")
        else:
            seen.add(probe_id)
        if signal.get("status") != "passing":
            violations.append(f"signal_{index}:status_must_be_passing")
        successes = signal.get("consecutive_successes")
        if not isinstance(successes, int) or isinstance(successes, bool) or successes < required_consecutive_successes:
            violations.append(f"signal_{index}:consecutive_successes_below_requirement")
        if _timestamp(signal.get("observed_at")) is None:
            violations.append(f"signal_{index}:observed_at_must_be_timezone_aware")
    if len(seen) < minimum_signals:
        violations.append("health_signal_quorum_not_met")
    return tuple(violations)


def health_signal_quorum_is_met(signals: list[object], **policy: object) -> bool:
    return not health_signal_quorum_violations(signals, **policy)


def _timestamp(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None and parsed.utcoffset() is not None else None
