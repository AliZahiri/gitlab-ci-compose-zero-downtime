from __future__ import annotations

from datetime import datetime
import re


_CHECKPOINTS = ("planned", "candidate_started", "health_checked", "traffic_switched", "verified")
_DIGEST = re.compile(r"sha256:[0-9a-f]{64}\Z")


def deployment_retry_violations(attempts: list[dict[str, object]], *, maximum_attempts: int = 5) -> tuple[str, ...]:
    if not isinstance(maximum_attempts, int) or isinstance(maximum_attempts, bool) or maximum_attempts < 2:
        raise ValueError("maximum_attempts must be an integer of at least two")
    if not isinstance(attempts, list) or len(attempts) < 2:
        return ("at_least_two_deployment_attempts_are_required",)
    violations: list[str] = []
    if len(attempts) > maximum_attempts:
        violations.append("deployment_retry_count_exceeds_policy")
    expected: tuple[object, ...] | None = None
    seen_attempts: set[str] = set()
    previous_checkpoint = -1
    previous_started_at: datetime | None = None
    for index, attempt in enumerate(attempts):
        if not isinstance(attempt, dict):
            violations.append(f"attempt_{index}:must_be_an_object")
            continue
        attempt_id = attempt.get("attempt_id")
        if not isinstance(attempt_id, str) or not attempt_id.strip():
            violations.append(f"attempt_{index}:attempt_id_is_required")
        elif attempt_id in seen_attempts:
            violations.append(f"attempt_{index}:attempt_id_must_be_unique")
        else:
            seen_attempts.add(attempt_id)
        identity = (attempt.get("deployment_id"), attempt.get("environment"), attempt.get("target_color"), attempt.get("image_digest"))
        if not all(isinstance(value, str) and value.strip() for value in identity[:2]):
            violations.append(f"attempt_{index}:deployment_and_environment_are_required")
        if identity[2] not in {"blue", "green"}:
            violations.append(f"attempt_{index}:target_color_is_invalid")
        if not isinstance(identity[3], str) or _DIGEST.fullmatch(identity[3]) is None:
            violations.append(f"attempt_{index}:image_digest_must_be_immutable")
        if expected is None:
            expected = identity
        elif identity != expected:
            violations.append(f"attempt_{index}:release_identity_changed_during_retry")
        checkpoint = attempt.get("last_completed_checkpoint")
        if checkpoint not in _CHECKPOINTS:
            violations.append(f"attempt_{index}:checkpoint_is_invalid")
        else:
            checkpoint_index = _CHECKPOINTS.index(checkpoint)
            if checkpoint_index < previous_checkpoint:
                violations.append(f"attempt_{index}:checkpoint_regressed")
            previous_checkpoint = checkpoint_index
        started_at = _timestamp(attempt.get("started_at"))
        if started_at is None:
            violations.append(f"attempt_{index}:started_at_must_be_timezone_aware")
        elif previous_started_at is not None and started_at <= previous_started_at:
            violations.append(f"attempt_{index}:attempt_time_must_increase")
        else:
            previous_started_at = started_at
    return tuple(violations)


def deployment_retry_is_safe(attempts: list[dict[str, object]], **policy: object) -> bool:
    return not deployment_retry_violations(attempts, **policy)


def _timestamp(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None and parsed.utcoffset() is not None else None
