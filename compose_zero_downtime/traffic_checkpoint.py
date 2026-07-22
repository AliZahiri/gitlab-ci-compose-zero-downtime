from __future__ import annotations

import re


_DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")


def traffic_checkpoint_violations(checkpoint: dict[str, object]) -> tuple[str, ...]:
    violations: list[str] = []
    current = checkpoint.get("current_color")
    candidate = checkpoint.get("candidate_color")
    if current not in {"blue", "green"} or candidate not in {"blue", "green"}:
        violations.append("deployment_colors_must_be_blue_or_green")
    elif current == candidate:
        violations.append("candidate_must_differ_from_current_color")
    digest = checkpoint.get("candidate_digest")
    if not isinstance(digest, str) or not _DIGEST.fullmatch(digest):
        violations.append("candidate_digest_must_be_immutable")
    if checkpoint.get("candidate_healthy") is not True:
        violations.append("candidate_health_must_be_confirmed")
    if checkpoint.get("proxy_config_valid") is not True:
        violations.append("proxy_configuration_must_be_validated")
    if not str(checkpoint.get("previous_upstream", "")).strip():
        violations.append("previous_upstream_is_required_for_rollback")
    return tuple(violations)


def traffic_checkpoint_is_ready(checkpoint: dict[str, object]) -> bool:
    return not traffic_checkpoint_violations(checkpoint)
