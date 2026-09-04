from __future__ import annotations

from datetime import datetime
import re


_SHA256 = re.compile(r"(?:sha256:)?[0-9a-f]{64}\Z")


def rendered_compose_provenance_violations(evidence: dict[str, object], *, expected_services: frozenset[str], now: datetime, maximum_age_seconds: int = 900) -> tuple[str, ...]:
    if not isinstance(expected_services, frozenset) or not expected_services or any(not isinstance(value, str) or not value.strip() for value in expected_services):
        raise ValueError("expected_services must be a non-empty frozenset of names")
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("current time must be timezone-aware")
    if not isinstance(maximum_age_seconds, int) or isinstance(maximum_age_seconds, bool) or maximum_age_seconds < 1:
        raise ValueError("maximum_age_seconds must be positive")
    if not isinstance(evidence, dict):
        return ("compose_provenance_evidence_must_be_an_object",)

    violations: list[str] = []
    for prefix in ("compose", "environment_contract"):
        reviewed = evidence.get(f"reviewed_{prefix}_sha256")
        deployed = evidence.get(f"deployed_{prefix}_sha256")
        if not isinstance(reviewed, str) or not _SHA256.fullmatch(reviewed):
            violations.append(f"reviewed_{prefix}_sha256_must_be_a_digest")
        if not isinstance(deployed, str) or not _SHA256.fullmatch(deployed):
            violations.append(f"deployed_{prefix}_sha256_must_be_a_digest")
        if isinstance(reviewed, str) and isinstance(deployed, str) and reviewed != deployed:
            violations.append(f"{prefix}_digest_does_not_match_reviewed_plan")
    services = evidence.get("services")
    if not isinstance(services, list) or any(not isinstance(value, str) or not value.strip() for value in services):
        violations.append("services_must_be_a_string_list")
    elif len(services) != len(set(services)) or set(services) != expected_services:
        violations.append("rendered_service_set_does_not_match_expected")
    observed_at = _timestamp(evidence.get("observed_at"))
    if observed_at is None or not 0 <= (now - observed_at).total_seconds() <= maximum_age_seconds:
        violations.append("compose_provenance_observation_is_invalid_stale_or_future_dated")
    return tuple(violations)


def rendered_compose_provenance_is_verified(evidence: dict[str, object], **policy: object) -> bool:
    return not rendered_compose_provenance_violations(evidence, **policy)


def _timestamp(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None and parsed.utcoffset() is not None else None
