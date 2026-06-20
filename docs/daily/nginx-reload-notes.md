# Document Nginx reload behavior

<!-- daily-pr-task: nginx-reload-notes -->

The traffic switch relies on rendering a new upstream and reloading Nginx. Reloading should apply the new config while keeping the proxy process available.

Operational notes:

- validate generated config before production use
- reload rather than stop/start where possible
- keep the old color running during the switch
- restart only as a fallback path

## Portfolio Value

Explains the reverse proxy behavior behind the Docker Compose zero-downtime pattern.

## Validation

Review the markdown file and confirm it separates reload from restart fallback.
