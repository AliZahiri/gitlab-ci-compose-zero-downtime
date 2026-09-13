from __future__ import annotations

from datetime import datetime

def _time(value: object) -> datetime | None:
    if not isinstance(value, str): return None
    try: parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
    except ValueError: return None
    return parsed if parsed.tzinfo and parsed.utcoffset() is not None else None

def rollback_execution_violations(evidence: object, *, failed_release: str, stable_release: str, now: datetime, maximum_age_seconds: int = 900) -> tuple[str, ...]:
    if not all(isinstance(value, str) and value.strip() for value in (failed_release, stable_release)) or failed_release == stable_release or now.tzinfo is None or maximum_age_seconds < 1: raise ValueError('invalid policy')
    if not isinstance(evidence, dict): return ('rollback_evidence_must_be_an_object',)
    violations: list[str] = []
    if evidence.get('failed_release') != failed_release: violations.append('failed_release_must_match_approved_release')
    if evidence.get('restored_release') != stable_release: violations.append('restored_release_must_match_last_stable_release')
    if evidence.get('rollback_succeeded') is not True: violations.append('rollback_must_succeed')
    if evidence.get('post_rollback_smoke_passed') is not True: violations.append('post_rollback_smoke_test_must_pass')
    observed = _time(evidence.get('observed_at'))
    if observed is None or not 0 <= (now-observed).total_seconds() <= maximum_age_seconds: violations.append('rollback_evidence_is_invalid_stale_or_future_dated')
    return tuple(violations)
