from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path
from urllib.parse import urljoin


VALID_COLORS = {"blue", "green"}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def read_active_color(active_file: Path) -> str:
    try:
        value = active_file.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        return "blue"
    return value if value in VALID_COLORS else "blue"


def choose_next_color(current_color: str, requested_color: str | None = None) -> str:
    if requested_color:
        if requested_color not in VALID_COLORS:
            raise ValueError("next color must be blue or green")
        return requested_color
    return "green" if current_color == "blue" else "blue"


def render_nginx_config(template: Path, output: Path, active_color: str, app_port: str) -> None:
    rendered = (
        template.read_text(encoding="utf-8")
        .replace("{{ACTIVE_COLOR}}", active_color)
        .replace("{{APP_PORT}}", app_port)
    )
    output.write_text(rendered, encoding="utf-8")


def build_smoke_url(base_url: str, path: str = "/") -> str:
    clean_base = base_url.rstrip("/") + "/"
    clean_path = path.lstrip("/")
    return urljoin(clean_base, clean_path)


def run_smoke_test(base_url: str, path: str, timeout: float) -> None:
    target = build_smoke_url(base_url, path)
    with urllib.request.urlopen(target, timeout=timeout) as response:
        if response.status >= 400:
            raise RuntimeError(f"smoke test failed with HTTP {response.status}: {target}")


def compose_command(compose_file: Path, env_file: Path, *args: str) -> list[str]:
    return ["docker", "compose", "-f", str(compose_file), "--env-file", str(env_file), *args]


def run(command: list[str], *, check: bool = True, capture: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        check=check,
        text=True,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.PIPE if capture else None,
    )


def get_container_id(compose_file: Path, env_file: Path, service: str) -> str:
    result = run(compose_command(compose_file, env_file, "ps", "-q", service), capture=True)
    container_id = result.stdout.strip()
    if not container_id:
        raise RuntimeError(f"Could not find {service} container")
    return container_id


def container_health(container_id: str) -> str:
    result = run(
        [
            "docker",
            "inspect",
            "--format",
            "{{if .State.Health}}{{.State.Health.Status}}{{else}}running{{end}}",
            container_id,
        ],
        capture=True,
    )
    return result.stdout.strip()


def wait_for_ready(container_id: str, service: str, attempts: int, interval: float) -> None:
    for _ in range(attempts):
        status = container_health(container_id)
        if status in {"healthy", "running"}:
            return
        if status == "unhealthy":
            run(["docker", "logs", container_id], check=False)
            raise RuntimeError(f"{service} is unhealthy")
        time.sleep(interval)
    raise TimeoutError(f"{service} did not become ready")


def deploy(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve() if args.root else repo_root()
    deploy_dir = root / "deploy"
    compose_file = Path(os.environ.get("COMPOSE_FILE", deploy_dir / "docker-compose.blue-green.yml"))
    env_file = Path(os.environ.get("ENV_FILE", root / ".env"))
    active_file = Path(os.environ.get("ACTIVE_FILE", deploy_dir / ".active-color"))
    app_port = os.environ.get("APP_PORT", "80")
    stop_old = os.environ.get("STOP_OLD_AFTER_SWITCH", "true").lower() == "true"

    current_color = read_active_color(active_file)
    next_color = choose_next_color(current_color, args.color)
    old_color = "" if current_color == next_color else current_color

    app_image = os.environ.get("APP_IMAGE")
    if app_image:
        os.environ[f"{next_color.upper()}_IMAGE"] = app_image

    service = f"app_{next_color}"
    print(f"Deploying {service}")
    run(compose_command(compose_file, env_file, "--profile", next_color, "up", "-d", service))

    container_id = get_container_id(compose_file, env_file, service)
    print(f"Waiting for {service} health check")
    wait_for_ready(container_id, service, args.health_attempts, args.health_interval)

    render_nginx_config(
        deploy_dir / "nginx/default.conf.tpl",
        deploy_dir / "nginx/default.conf",
        next_color,
        app_port,
    )

    run(compose_command(compose_file, env_file, "--profile", next_color, "up", "-d", "nginx"))
    reload_result = run(
        compose_command(compose_file, env_file, "exec", "-T", "nginx", "nginx", "-s", "reload"),
        check=False,
    )
    if reload_result.returncode != 0:
        run(compose_command(compose_file, env_file, "restart", "nginx"))

    active_file.write_text(f"{next_color}\n", encoding="utf-8")
    print(f"Traffic switched to {next_color}")

    if args.smoke_url:
        print(f"Running public smoke test against {build_smoke_url(args.smoke_url, args.smoke_path)}")
        run_smoke_test(args.smoke_url, args.smoke_path, args.smoke_timeout)

    if old_color and stop_old:
        run(compose_command(compose_file, env_file, "stop", f"app_{old_color}"), check=False)

    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Docker Compose blue/green deployment helper")
    subparsers = parser.add_subparsers(dest="command", required=True)

    deploy_parser = subparsers.add_parser("deploy", help="Deploy and promote the inactive color")
    deploy_parser.add_argument("color", nargs="?", choices=sorted(VALID_COLORS))
    deploy_parser.add_argument("--root", help="Repository root. Defaults to the current package root.")
    deploy_parser.add_argument("--health-attempts", type=int, default=60)
    deploy_parser.add_argument("--health-interval", type=float, default=2.0)
    deploy_parser.add_argument("--smoke-url", help="Public base URL to verify after switching traffic.")
    deploy_parser.add_argument("--smoke-path", default="/", help="Public path used for the smoke test.")
    deploy_parser.add_argument("--smoke-timeout", type=float, default=5.0)
    deploy_parser.set_defaults(func=deploy)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
