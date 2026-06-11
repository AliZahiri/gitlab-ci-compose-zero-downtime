# GitLab CI Docker Compose Zero-Downtime Templates

Reusable GitLab CI and Docker Compose deployment templates for production-style services.

The main pattern is blue/green deployment behind a reverse proxy. The new version starts first, passes health checks, then traffic is switched by reloading Nginx. This can provide zero-downtime traffic switching for HTTP services when the application is stateless, health checks are reliable, and database changes are backward compatible.

## What This Shows

- GitLab CI pipeline structure for Docker build, push, and deploy
- Docker Compose based blue/green deployment
- Health-check-gated release promotion
- Nginx upstream switch without stopping the active service first
- Rollback-friendly deployment layout
- Practical notes for secrets, migrations, and production operations

## Repository Structure

```text
.
├── deploy/
│   ├── blue-green-deploy.sh
│   ├── docker-compose.blue-green.yml
│   └── nginx/
│       ├── default.conf
│       └── default.conf.tpl
├── docs/
│   └── zero-downtime-compose.md
├── examples/
│   └── backend/
│       └── .gitlab-ci.yml
└── templates/
    ├── compose-blue-green-deploy.yml
    └── docker-build.yml
```

## Deployment Flow

```text
GitLab CI
   |
   v
Build image -> Push image -> SSH deploy
   |
   v
Start inactive color
   |
   v
Wait for container health check
   |
   v
Render Nginx upstream to new color
   |
   v
Reload Nginx
   |
   v
Stop old color after traffic switch
```

## Local Demo

```bash
cp .env.example .env
docker compose -f deploy/docker-compose.blue-green.yml --env-file .env --profile blue up -d
echo blue > deploy/.active-color
./deploy/blue-green-deploy.sh green
```

## GitLab CI Usage

In a service repository:

```yaml
include:
  - project: platform/gitlab-ci-compose-zero-downtime
    file:
      - templates/docker-build.yml
      - templates/compose-blue-green-deploy.yml
```

Required CI/CD variables:

- `CI_REGISTRY_USER`
- `CI_REGISTRY_PASSWORD`
- `DEPLOY_HOST`
- `DEPLOY_USER`
- `DEPLOY_PATH`
- `SSH_PRIVATE_KEY`
- `APP_IMAGE`

## Production Requirements

- The application must expose a reliable health endpoint.
- The reverse proxy must reload config without dropping active connections.
- Old and new app versions must be able to run at the same time.
- Database migrations must be backward compatible.
- Persistent state must live outside the app container.
- Secrets must be injected through GitLab CI/CD variables or server-side env files.

See [docs/zero-downtime-compose.md](docs/zero-downtime-compose.md).
