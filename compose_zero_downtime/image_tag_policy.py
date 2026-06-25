from __future__ import annotations


def image_tag_warnings(image: str) -> tuple[str, ...]:
    value = image.strip()
    warnings: list[str] = []
    if not value:
        return ("image_missing",)
    if value.endswith(":latest") or value == "latest":
        warnings.append("latest_tag_is_not_immutable")
    if "@sha256:" not in value and ":" not in value.rsplit("/", 1)[-1]:
        warnings.append("image_must_use_digest_or_explicit_tag")
    return tuple(warnings)


def image_tag_is_immutable(image: str) -> bool:
    return not image_tag_warnings(image)
