from __future__ import annotations

REQUIRED_COLOR_PROFILES = ("blue", "green")


def missing_color_profiles(profiles: list[str] | tuple[str, ...] | set[str]) -> tuple[str, ...]:
    present = set(profiles)
    return tuple(profile for profile in REQUIRED_COLOR_PROFILES if profile not in present)


def compose_profiles_are_ready(profiles: list[str] | tuple[str, ...] | set[str]) -> bool:
    return not missing_color_profiles(profiles)
