# Add deployment credential redaction evidence gate

<!-- daily-pr-task: deployment-credential-redaction-evidence-gate -->

Deployment logs and plan artifacts can leak credentials even when secret files are never committed. This offline evidence gate requires a versioned scanner, completed scan, coverage of sensitive field categories, zero exposed findings, and an immutable artifact identifier without storing secret values.

## Portfolio Value

Adds auditable secret-leak prevention for dry-run plans and deployment logs without embedding credentials or depending on a live secret manager in CI.

## Validation

Run python3 -m unittest discover -s tests and confirm a versioned complete clean scan passes while missing metadata, incomplete category coverage, unfinished scans, malformed evidence, and exposed findings fail.
