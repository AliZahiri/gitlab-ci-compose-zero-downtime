# Zero-Downtime With Docker Compose

Docker Compose does not provide Kubernetes-style rolling updates by itself. A reliable pattern is to keep two app targets available behind a reverse proxy:

- `app_blue`
- `app_green`

The deployment script starts the inactive color, waits for its health check, renders the reverse-proxy upstream to the new color, reloads the proxy, and only then stops the old color.

## Requirements

- App containers must start without binding directly to the public host port.
- The reverse proxy owns the public port.
- Health checks must represent real readiness, not only process liveness.
- The old and new versions must be able to run side by side.
- Migrations must be backward compatible.
- Sessions should be stateless or stored outside the app container.

## Rollback

Rollback is the same switch in reverse:

```bash
./deploy/blue-green-deploy.sh blue
```

or

```bash
./deploy/blue-green-deploy.sh green
```

depending on the last known healthy color.

## Limits

This pattern does not protect against:

- Breaking database migrations
- Shared-volume schema changes
- Stateful in-memory sessions
- Slow shutdown handlers that drop active requests
- Reverse proxy misconfiguration

It is still a strong deployment pattern for many small and medium production workloads that run on Docker Compose.
