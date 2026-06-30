from __future__ import annotations

REQUIRED_RELEASE_METADATA = ("commit_sha", "image", "target_color", "deploy_actor")
VALID_COLORS = {"blue", "green"}


def missing_release_metadata(metadata: dict[str, object]) -> tuple[str, ...]:
    return tuple(field for field in REQUIRED_RELEASE_METADATA if not metadata.get(field))


def release_metadata_warnings(metadata: dict[str, object]) -> tuple[str, ...]:
    warnings = list(missing_release_metadata(metadata))
    commit_sha = str(metadata.get("commit_sha", ""))
    if commit_sha and len(commit_sha) < 7:
        warnings.append("commit_sha_too_short")
    if metadata.get("target_color") and metadata.get("target_color") not in VALID_COLORS:
        warnings.append("target_color_must_be_blue_or_green")
    return tuple(warnings)


def release_metadata_is_complete(metadata: dict[str, object]) -> bool:
    return not release_metadata_warnings(metadata)
