#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPOSE_FILE="${COMPOSE_FILE:-$SCRIPT_DIR/docker-compose.blue-green.yml}"
ENV_FILE="${ENV_FILE:-$SCRIPT_DIR/../.env}"
ACTIVE_FILE="${ACTIVE_FILE:-$SCRIPT_DIR/.active-color}"
APP_PORT="${APP_PORT:-80}"
STOP_OLD_AFTER_SWITCH="${STOP_OLD_AFTER_SWITCH:-true}"

current_color="$(cat "$ACTIVE_FILE" 2>/dev/null || echo blue)"
requested_color="${1:-}"

if [[ -n "$requested_color" ]]; then
  next_color="$requested_color"
elif [[ "$current_color" == "blue" ]]; then
  next_color="green"
else
  next_color="blue"
fi

if [[ "$next_color" != "blue" && "$next_color" != "green" ]]; then
  echo "next color must be blue or green"
  exit 1
fi

if [[ "$current_color" == "$next_color" ]]; then
  old_color=""
else
  old_color="$current_color"
fi

if [[ -n "${APP_IMAGE:-}" ]]; then
  if [[ "$next_color" == "blue" ]]; then
    export BLUE_IMAGE="$APP_IMAGE"
  else
    export GREEN_IMAGE="$APP_IMAGE"
  fi
fi

echo "Deploying $next_color environment"
docker compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" --profile "$next_color" up -d "app_$next_color"

container_id="$(docker compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" ps -q "app_$next_color")"
if [[ -z "$container_id" ]]; then
  echo "Could not find app_$next_color container"
  exit 1
fi

echo "Waiting for app_$next_color health check"
for _ in $(seq 1 60); do
  status="$(docker inspect --format '{{if .State.Health}}{{.State.Health.Status}}{{else}}running{{end}}' "$container_id")"
  if [[ "$status" == "healthy" || "$status" == "running" ]]; then
    break
  fi
  if [[ "$status" == "unhealthy" ]]; then
    docker logs "$container_id" || true
    echo "app_$next_color is unhealthy"
    exit 1
  fi
  sleep 2
done

sed \
  -e "s/{{ACTIVE_COLOR}}/$next_color/g" \
  -e "s/{{APP_PORT}}/$APP_PORT/g" \
  "$SCRIPT_DIR/nginx/default.conf.tpl" > "$SCRIPT_DIR/nginx/default.conf"

docker compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" --profile "$next_color" up -d nginx
docker compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" exec -T nginx nginx -s reload || \
  docker compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" restart nginx

echo "$next_color" > "$ACTIVE_FILE"
echo "Traffic switched to $next_color"

if [[ -n "$old_color" && "$STOP_OLD_AFTER_SWITCH" == "true" ]]; then
  docker compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" stop "app_$old_color" || true
fi
