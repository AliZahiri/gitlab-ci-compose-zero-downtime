from __future__ import annotations


def missing_environment_keys(environment: dict[str, str], required_keys: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(key for key in required_keys if not environment.get(key, "").strip())


def environment_contract_is_ready(environment: dict[str, str], required_keys: tuple[str, ...]) -> bool:
    return not missing_environment_keys(environment, required_keys)
