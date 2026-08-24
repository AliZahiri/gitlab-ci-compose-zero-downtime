# Add release SBOM attestation gate

<!-- daily-pr-task: release-sbom-attestation-gate -->

Immutable deployment evidence should bind an SBOM to the exact release artifact. This offline gate validates SHA-256 subject and SBOM digests, an accepted SBOM format, signature verification, and a timezone-aware generation timestamp.

## Portfolio Value

Connects software supply-chain evidence to the immutable artifact already used by the blue-green release path without contacting a registry in CI.

## Validation

Run python3 -m unittest discover -s tests and confirm only a signed supported SBOM bound to the exact release digest passes.
