# Add Compose bind mount safety gate

<!-- daily-pr-task: compose-bind-mount-safety-gate -->

Bind mounts can silently expand a container's host access. This offline gate validates declared bind-mount metadata: each mount has an absolute source and target, comes from an explicitly approved host root, is not a sensitive host path such as the Docker socket, and is read-only. It evaluates plan metadata and does not parse or run Docker Compose.

## Portfolio Value

Adds a practical host-access boundary to the Compose deployment controls, demonstrating that a health-gated promotion also constrains what containers can read from the node.

## Validation

Run `python3 -m unittest discover -s tests` and confirm approved read-only mounts pass while empty manifests, dangerous host paths, unapproved roots, invalid paths, writable mounts, and invalid root policies fail.
