# Add dual-color resource headroom gate

<!-- daily-pr-task: dual-color-resource-headroom-gate -->

Blue-green deployment temporarily runs both colors, so a host that is healthy under one color can fail while starting the candidate. This deterministic preflight validates memory and disk observations, reserves an operator-defined safety margin, and blocks promotion when available capacity cannot cover the candidate color. It reads supplied metrics only and does not contact Docker or mutate a host.

## Portfolio Value

Prevents candidate startup from exhausting the host that still serves the active color by requiring explicit memory, disk, and safety-margin evidence before deployment.

## Validation

Run `python3 -m unittest discover -s tests` and confirm sufficient memory/disk headroom passes while missing observations, invalid measurements, insufficient reserved capacity, and invalid margin policy values fail.
