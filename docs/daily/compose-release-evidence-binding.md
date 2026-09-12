# Bind deployment evidence to the approved environment and immutable image

<!-- daily-pr-task: compose-release-evidence-binding -->

Stops cross-environment or previous-release evidence from authorizing a Compose promotion.

This offline control matches environment, release_id, image_digest against an externally reviewed expected contract and requires a timezone-aware observation inside a bounded freshness window. Digest values use sha256:<64 lowercase hex characters>. Evidence must be collected after the relevant checks run; matching metadata does not prove those checks were executed or provide cryptographic authenticity.

The JSON manifest has expected and evidence objects. Expected contains exactly the binding fields; evidence repeats them and includes observed_at. Run python3 scripts/compose_release_evidence_binding.py manifest.json --now 2026-09-12T06:00:00Z. Output is deterministic JSON; exit codes are 0 (passed), 1 (policy rejected), and 2 (invalid input or policy). The command makes no network or paid provider calls. Never put prompts, credentials, private host data, or customer documents into this manifest.

## Portfolio Value

Stops cross-environment or previous-release evidence from authorizing a Compose promotion.

## Validation

Run PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests. Verify binding mismatches, timestamp boundaries, invalid policies, malformed manifests, and CLI exit codes.
