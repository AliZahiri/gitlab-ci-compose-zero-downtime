# Add release artifact provenance gate

<!-- daily-pr-task: release-artifact-provenance-gate -->

An immutable image digest does not establish which build produced it or whether its SBOM and attestation refer to the same subject. This offline promotion gate validates unique image identities, OCI SHA-256 digests, verified signatures, and exact subject agreement across image, SBOM, and provenance evidence. It consumes CI metadata only and does not contact a registry.

## Portfolio Value

Strengthens immutable deployment guarantees by binding the promoted image, SBOM, build provenance, and signature verification to one reviewable OCI digest.

## Validation

Run `python3 -m unittest discover -s tests` and confirm matching signed artifacts pass while empty input, duplicate images, malformed digests, subject mismatches, and unverified signatures fail.
