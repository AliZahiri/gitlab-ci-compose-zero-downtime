from __future__ import annotations


def proxy_cache_bypass_violations(paths: object, *, strategy: object) -> tuple[str, ...]:
    if strategy not in {"bypass", "color_scoped_cache_key"}:
        return ("cache_strategy_must_be_explicit",)
    if not isinstance(paths, list) or not paths:
        return ("at_least_one_promotion_path_is_required",)
    violations: list[str] = []
    seen: set[str] = set()
    for index, path in enumerate(paths):
        if not isinstance(path, str) or not path.startswith("/") or path in seen:
            violations.append(f"path_{index}_must_be_a_unique_absolute_path")
        else:
            seen.add(path)
    return tuple(violations)

def proxy_cache_bypass_is_safe(paths: object, **policy: object) -> bool:
    return not proxy_cache_bypass_violations(paths, **policy)
