# Add release metadata policy

<!-- daily-pr-task: release-metadata-policy -->

A zero-downtime deployment should record enough release metadata to explain what changed and how to roll it back. Metadata should travel with CI logs and release notes.

Required metadata:

- commit sha
- image reference
- target color
- deploy actor

## Portfolio Value

Makes releases auditable by requiring commit, image, and deployment color metadata.

## Validation

Run the unit test and confirm missing release metadata is reported.
