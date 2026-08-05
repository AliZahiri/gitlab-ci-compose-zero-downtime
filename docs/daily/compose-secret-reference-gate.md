# Add Compose secret reference gate

<!-- daily-pr-task: compose-secret-reference-gate -->

A deployment plan should not embed sensitive credentials in a Compose environment block. This offline gate inspects supplied service metadata and requires sensitive environment values to be variable references or _FILE values rooted in the configured Docker secrets mount. It validates static manifest intent only; it neither resolves environment variables nor reads secret files.

## Portfolio Value

Prevents static credential leakage in a Compose release plan while keeping secret delivery explicit and compatible with Docker secrets-style file mounts.

## Validation

Run `python3 -m unittest discover -s tests` and confirm variable or /run/secrets references pass while embedded sensitive values, malformed secret paths, invalid manifests, and invalid mount-root policy fail.
