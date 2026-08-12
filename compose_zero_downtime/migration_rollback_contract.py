from __future__ import annotations


def migration_rollback_contract_violations(migrations: list[dict[str, object]]) -> tuple[str, ...]:
    if not migrations:
        return ("at_least_one_migration_is_required",)
    violations: list[str] = []
    seen_ids: set[str] = set()
    for index, migration in enumerate(migrations):
        migration_id = migration.get("migration_id")
        if not isinstance(migration_id, str) or not migration_id.strip():
            violations.append(f"migration_{index}:migration_id_is_required")
        elif migration_id in seen_ids:
            violations.append(f"migration_{index}:migration_id_must_be_unique")
        seen_ids.add(migration_id)
        if migration.get("forward_compatible") is not True:
            violations.append(f"migration_{index}:must_be_forward_compatible")
        if migration.get("rollback_strategy") not in {"restore_backup", "compensating_migration", "no_schema_change"}:
            violations.append(f"migration_{index}:rollback_strategy_must_be_explicit")
        if migration.get("backup_verified") is not True:
            violations.append(f"migration_{index}:backup_must_be_verified")
    return tuple(violations)


def migration_rollback_contract_is_safe(migrations: list[dict[str, object]]) -> bool:
    return not migration_rollback_contract_violations(migrations)
