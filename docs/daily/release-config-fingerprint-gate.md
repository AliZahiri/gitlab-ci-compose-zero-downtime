# Add release config fingerprint gate

<!-- daily-pr-task: release-config-fingerprint-gate -->

A validated deployment plan is not trustworthy if the Compose, proxy, or environment contract changes before promotion. This offline gate compares planned and observed SHA-256 fingerprints for every required component and requires rollback fingerprints to remain available. It evaluates supplied metadata only and never reads secrets or mutates a deployment.

## Portfolio Value

Detects configuration drift between validated plans and promotion while preserving explicit rollback evidence for Compose, proxy, and environment contracts.

## Validation

Run `python3 -m unittest discover -s tests` and confirm matching SHA-256 evidence passes while missing components, malformed fingerprints, plan/observation drift, absent rollback fingerprints, and invalid component policy fail.
