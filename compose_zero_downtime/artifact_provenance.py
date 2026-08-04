from __future__ import annotations

import re


_DIGEST = re.compile(r"sha256:[0-9a-f]{64}\Z")


def artifact_provenance_violations(artifacts: list[dict[str, object]]) -> tuple[str, ...]:
    if not artifacts:
        return ("at_least_one_release_artifact_is_required",)
    violations: list[str] = []
    seen: set[str] = set()
    for position, artifact in enumerate(artifacts):
        image = str(artifact.get("image", "")).strip()
        if not image:
            violations.append(f"artifact_{position}:image_is_required")
        elif image in seen:
            violations.append(f"artifact_{position}:image_must_be_unique")
        seen.add(image)
        digest = artifact.get("image_digest")
        sbom_subject = artifact.get("sbom_subject_digest")
        provenance_subject = artifact.get("provenance_subject_digest")
        for field, value in (("image_digest", digest), ("sbom_subject_digest", sbom_subject), ("provenance_subject_digest", provenance_subject)):
            if not isinstance(value, str) or not _DIGEST.fullmatch(value):
                violations.append(f"artifact_{position}:{field}_must_be_an_oci_sha256_digest")
        if isinstance(digest, str) and _DIGEST.fullmatch(digest):
            if sbom_subject != digest:
                violations.append(f"artifact_{position}:sbom_subject_digest_mismatch")
            if provenance_subject != digest:
                violations.append(f"artifact_{position}:provenance_subject_digest_mismatch")
        if artifact.get("signature_verified") is not True:
            violations.append(f"artifact_{position}:signature_must_be_verified")
    return tuple(violations)


def release_artifacts_have_provenance(artifacts: list[dict[str, object]]) -> bool:
    return not artifact_provenance_violations(artifacts)
