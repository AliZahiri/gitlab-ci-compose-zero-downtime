from __future__ import annotations

REQUIRED_RELEASE_METADATA = ("commit_sha", "image", "target_color", "deploy_actor")


def missing_release_metadata(metadata: dict[str, object]) -> tuple[str, ...]:
    return tuple(field for field in REQUIRED_RELEASE_METADATA if not metadata.get(field))


def release_metadata_is_complete(metadata: dict[str, object]) -> bool:
    return not missing_release_metadata(metadata)
