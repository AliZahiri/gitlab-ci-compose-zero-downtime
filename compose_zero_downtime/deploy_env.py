from __future__ import annotations

REQUIRED_DEPLOY_ENV_VARS = (
    "DEPLOY_HOST",
    "DEPLOY_USER",
    "DEPLOY_PATH",
    "APP_IMAGE",
    "APP_PORT",
)


def missing_deploy_env_vars(env: dict[str, str]) -> tuple[str, ...]:
    return tuple(name for name in REQUIRED_DEPLOY_ENV_VARS if not env.get(name))


def deploy_env_is_complete(env: dict[str, str]) -> bool:
    return not missing_deploy_env_vars(env)
