from __future__ import annotations

import re


SEMVER_TAG_PATTERN = re.compile(r"^v?\d+\.\d+\.\d+(?:[-+][A-Za-z0-9.-]+)?$")


def image_reference_tag(image: str) -> str:
    reference = image.strip().rsplit("/", 1)[-1]
    if ":" not in reference:
        return ""
    return reference.rsplit(":", 1)[-1]


def image_tag_warnings(image: str) -> tuple[str, ...]:
    value = image.strip()
    warnings: list[str] = []
    if not value:
        return ("image_missing",)
    if value.endswith(":latest") or value == "latest":
        warnings.append("latest_tag_is_not_immutable")
    tag = image_reference_tag(value)
    if "@sha256:" not in value and not tag:
        warnings.append("image_must_use_digest_or_explicit_tag")
    if tag and tag != "latest" and not SEMVER_TAG_PATTERN.fullmatch(tag):
        warnings.append("image_tag_should_be_semver")
    return tuple(warnings)


def image_tag_is_immutable(image: str) -> bool:
    return not image_tag_warnings(image)
