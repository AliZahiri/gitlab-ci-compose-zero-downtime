from __future__ import annotations


_REQUIRED_CONFIRMATIONS = ("candidate_healthy", "proxy_config_validated", "smoke_tests_passed", "traffic_switch_succeeded", "rollback_ready")


def promotion_evidence_violations(evidence: dict[str, object], *, minimum_health_samples: int = 3) -> tuple[str, ...]:
    if not isinstance(minimum_health_samples, int) or isinstance(minimum_health_samples, bool) or minimum_health_samples <= 0:
        raise ValueError("minimum health samples must be a positive integer")
    violations: list[str] = []
    if not str(evidence.get("release_id", "")).strip():
        violations.append("release_id_is_required")
    current = evidence.get("current_color")
    candidate = evidence.get("candidate_color")
    if current not in {"blue", "green"} or candidate not in {"blue", "green"}:
        violations.append("deployment_colors_must_be_blue_or_green")
    elif current == candidate:
        violations.append("candidate_color_must_differ_from_current_color")
    samples = evidence.get("successful_health_samples")
    if not isinstance(samples, int) or isinstance(samples, bool) or samples < minimum_health_samples:
        violations.append("successful_health_samples_below_minimum")
    for field in _REQUIRED_CONFIRMATIONS:
        if evidence.get(field) is not True:
            violations.append(f"{field}_must_be_confirmed")
    return tuple(violations)


def promotion_evidence_is_complete(evidence: dict[str, object], *, minimum_health_samples: int = 3) -> bool:
    return not promotion_evidence_violations(evidence, minimum_health_samples=minimum_health_samples)
