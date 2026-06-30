from __future__ import annotations

REQUIRED_AUDIT_FIELDS = ("actor", "commit_sha", "image", "target_color", "result")


def missing_audit_fields(event: dict[str, object]) -> tuple[str, ...]:
    return tuple(field for field in REQUIRED_AUDIT_FIELDS if not event.get(field))


def deploy_audit_event_is_complete(event: dict[str, object]) -> bool:
    return not missing_audit_fields(event)
