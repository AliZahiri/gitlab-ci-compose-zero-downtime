from __future__ import annotations

import re


_DIGEST = re.compile(r"sha256:[0-9a-f]{64}\b")


def rollback_command_contract_violations(contract: dict[str, object], *, known_colors: set[str]) -> tuple[str, ...]:
    if not known_colors:
        raise ValueError("at least one known color is required")
    violations: list[str] = []
    command = contract.get("command")
    if not isinstance(command, str) or not command.strip():
        violations.append("command_is_required")
    elif not _DIGEST.search(command):
        violations.append("command_must_reference_immutable_image_digest")
    color = contract.get("target_color")
    if color not in known_colors:
        violations.append("target_color_must_be_known")
    verification = contract.get("verification_command")
    if not isinstance(verification, str) or not verification.strip():
        violations.append("verification_command_is_required")
    return tuple(violations)


def rollback_command_contract_is_safe(contract: dict[str, object], *, known_colors: set[str]) -> bool:
    return not rollback_command_contract_violations(contract, known_colors=known_colors)
