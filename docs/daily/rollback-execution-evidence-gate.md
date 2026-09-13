# Add rollback execution evidence gate

<!-- daily-pr-task: rollback-execution-evidence-gate -->

A rollback plan is credible only when a successful recovery is tied to the failed
release, the approved last-stable release, a passing post-rollback smoke check,
and a fresh observation time. This offline gate rejects stale or mismatched
rollback evidence without inspecting production traffic or credentials.

## Evidence contract

The manifest contains exactly two approved release identifiers under `expected`.
The `evidence` object records the observed rollback outcome:

```json
{
  "expected": {
    "failed_release": "orders-20260913.2",
    "stable_release": "orders-20260913.1"
  },
  "evidence": {
    "failed_release": "orders-20260913.2",
    "restored_release": "orders-20260913.1",
    "rollback_succeeded": true,
    "post_rollback_smoke_passed": true,
    "observed_at": "2026-09-13T11:55:00Z"
  }
}
```

Evaluate the manifest against an explicit, timezone-aware decision time:

```bash
python3 scripts/validate_rollback_execution.py rollback.json \
  --now 2026-09-13T12:00:00Z \
  --maximum-age-seconds 900
```

The command emits deterministic JSON. Exit code `0` means the evidence passed,
`1` means the rollback claim was rejected by policy, and `2` means the manifest
or policy input was invalid. It performs no network calls.

## Trust boundary

This validator checks consistency and freshness; it does not perform the rollback
or prove that the evidence producer is trustworthy. Production use should collect
the evidence from an authenticated deployment system, protect it from mutation,
and bind the approved identifiers to immutable release metadata.

Never place credentials, private host data, or customer payloads in the manifest.

## Portfolio Value

Connects rollback readiness to a reviewable successful recovery and smoke-test
result, rather than treating a declared rollback target as proof.

## Validation

Run `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests`. Confirm
that release mismatches, false outcome claims, malformed manifests, naive/future/
stale timestamps, and invalid policy values fail closed while exact age boundaries
and equivalent timezone offsets pass.
