# Add blue-green volume write isolation contract gate

<!-- daily-pr-task: blue-green-volume-write-isolation-contract-gate -->

Blue and green application stacks must not concurrently mutate the same volume during candidate verification. This offline gate validates unique mount targets per color and rejects shared writable sources while permitting explicitly read-only shared configuration or trust bundles.

## Portfolio Value

Closes a practical blue-green data-corruption risk by making concurrent volume ownership explicit before health checks and traffic promotion.

## Validation

Run python3 -m unittest discover -s tests and confirm distinct writable volumes and shared read-only assets pass while shared writes, malformed mounts, relative paths, and duplicate targets fail.
