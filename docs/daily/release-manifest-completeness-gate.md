# Add release manifest completeness gate

<!-- daily-pr-task: release-manifest-completeness-gate -->

A deployment record must link the promoted image to its source revision and rendered configuration. This offline gate validates release manifests: a stable release ID, immutable image digest, full source revision, configuration SHA-256, and timezone-aware creation time. It never resolves a registry or repository.

## Portfolio Value

Improves release traceability by binding source, artifact, configuration, and time into one reviewable promotion record.

## Validation

Run `python3 -m unittest discover -s tests` and confirm a complete immutable manifest passes while absent IDs, mutable artifacts, short revisions, invalid configuration hashes, and naive timestamps fail.
