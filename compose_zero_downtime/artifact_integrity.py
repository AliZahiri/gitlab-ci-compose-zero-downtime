from __future__ import annotations

REQUIRED_ARTIFACT_FIELDS = ("image", "digest", "build_id", "source_revision")


def artifact_integrity_warnings(artifact: dict[str, object]) -> tuple[str, ...]:
    warnings: list[str] = []
    for field in REQUIRED_ARTIFACT_FIELDS:
        if not str(artifact.get(field, "")).strip():
            warnings.append(f"{field}_is_required")
    digest = str(artifact.get("digest", "")).strip()
    if digest and not digest.startswith("sha256:"):
        warnings.append("digest_must_use_sha256")
    return tuple(warnings)


def artifact_is_promotable(artifact: dict[str, object]) -> bool:
    return not artifact_integrity_warnings(artifact)
