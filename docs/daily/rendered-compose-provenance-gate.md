# Add rendered Compose provenance gate

<!-- daily-pr-task: rendered-compose-provenance-gate -->

A reviewed Compose source file does not prove that interpolation and override selection produced the same deployment plan at runtime. This offline gate compares reviewed and deployed rendered-config digests, environment-contract digests, and exact service membership using fresh evidence. It accepts hashes and service names only, never environment values or secrets.

## Portfolio Value

Connects code review to the actual interpolated Compose plan so unreviewed overrides, service injection, and environment-contract drift block promotion.

## Validation

Run python3 -m unittest discover -s tests and confirm only a fresh rendered plan with matching reviewed/deployed digests and the exact expected service set passes.
