# Add Nginx upstream target parity gate

<!-- daily-pr-task: nginx-upstream-target-parity-gate -->

A successful Nginx syntax check does not prove that the rendered upstream points only to the intended candidate containers. This deterministic gate compares normalized expected and rendered target sets, rejects duplicates, and requires successful proxy validation before promotion. It evaluates supplied plan evidence without reloading Nginx.

## Portfolio Value

Closes the gap between syntactically valid proxy configuration and the actual blue-green plan by proving that no stale or unintended target is rendered for promotion.

## Validation

Run `python3 -m unittest discover -s tests` and confirm exact candidate target parity passes while invalid config, duplicate or empty targets, missing candidates, unexpected old-color targets, and malformed plans fail.
