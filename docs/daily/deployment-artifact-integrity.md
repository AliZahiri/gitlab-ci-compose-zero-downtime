# Add deployment artifact integrity guard

<!-- daily-pr-task: deployment-artifact-integrity -->

A blue-green release should promote a traceable image artifact, not an ambiguous mutable tag. The deployment plan can fail before traffic moves when the image digest, build identifier, or provenance marker is missing.

Integrity signals:

- image digest uses sha256
- build identifier is present
- source revision is recorded
- emergency bypass remains explicit

## Portfolio Value

Adds a release-safety control that makes the Docker Compose deployment story more production credible.

## Validation

Run `python3 -m unittest discover -s tests` and confirm mutable artifacts are rejected before promotion.
