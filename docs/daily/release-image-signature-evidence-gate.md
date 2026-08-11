# Add release image signature evidence gate

<!-- daily-pr-task: release-image-signature-evidence-gate -->

Image provenance should include verifiable signing evidence before a blue/green promotion. This offline gate validates supplied release evidence: immutable image digest, trusted signer identity, successful signature verification, and a timezone-aware verification timestamp. It does not contact a registry or run a signature verifier.

## Portfolio Value

Completes immutable artifact validation with reviewable signing evidence before an image is allowed to replace production traffic.

## Validation

Run `python3 -m unittest discover -s tests` and confirm trusted immutable verified image evidence passes while mutable digests, untrusted signers, missing verification, naive timestamps, and invalid signer policy fail.
