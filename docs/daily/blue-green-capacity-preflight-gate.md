# Add blue-green capacity preflight gate

<!-- daily-pr-task: blue-green-capacity-preflight-gate -->

A healthy candidate is not enough for a safe blue-green promotion if it cannot absorb expected traffic while the old color remains available for rollback. This offline preflight validates distinct colors, healthy replica counts, spare connection capacity, and reserved rollback capacity from aggregate deployment evidence. It does not contact a runtime or inspect request payloads.

## Portfolio Value

Prevents promotion based on nominal health alone by requiring capacity for expected traffic and a viable rollback window during dual-color operation.

## Validation

Run python3 -m unittest discover -s tests and confirm only distinct healthy colors with sufficient connection headroom, health quorum, and reserved rollback capacity pass.
