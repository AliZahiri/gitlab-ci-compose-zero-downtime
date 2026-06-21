from __future__ import annotations


def nginx_reload_commands(*, validate_config: bool = True) -> tuple[list[str], list[str]]:
    reload_command = ["nginx", "-s", "reload"]
    if validate_config:
        reload_command = ["nginx", "-t", "&&", *reload_command]
    fallback_command = ["docker", "compose", "restart", "nginx"]
    return reload_command, fallback_command


def reload_is_preferred_over_restart(commands: tuple[list[str], list[str]]) -> bool:
    reload_command, fallback_command = commands
    return "reload" in reload_command and "restart" in fallback_command
