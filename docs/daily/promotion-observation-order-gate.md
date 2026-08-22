# Add promotion observation ordering gate

<!-- daily-pr-task: promotion-observation-order-gate -->

Validate that health evidence, traffic switch evidence, and post-promotion observation are recorded in a safe order before a blue-green release is declared complete.

## Portfolio Value

Captures the ordering dependency between health proof, traffic promotion, and post-switch verification instead of treating them as independent checklist items.

## Validation

Run `python3 -m unittest discover -s tests` and confirm missing or reordered promotion evidence fails.
