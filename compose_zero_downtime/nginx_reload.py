from __future__ import annotations


def nginx_reload_commands(*, validate_config: bool = True) -> tuple[list[list[str]], list[str]]:
    reload_commands: list[list[str]] = []
    if validate_config:
        reload_commands.append(["nginx", "-t"])
    reload_commands.append(["nginx", "-s", "reload"])
    fallback_command = ["docker", "compose", "restart", "nginx"]
    return reload_commands, fallback_command


def reload_is_preferred_over_restart(commands: tuple[list[list[str]], list[str]]) -> bool:
    reload_commands, fallback_command = commands
    has_reload_step = any(command[-2:] == ["-s", "reload"] for command in reload_commands)
    return has_reload_step and "restart" in fallback_command
