# Add candidate restart stability evidence gate

<!-- daily-pr-task: candidate-restart-stability-evidence-gate -->

A container can answer a health probe between crashes and still be unsafe to promote. This offline gate compares candidate container restart counters with the start of the observation window, rejects OOM termination, requires every expected container to remain running, and validates evidence freshness before traffic promotion.

## Portfolio Value

Closes the gap between point-in-time health checks and sustained candidate stability by making restart and OOM evidence part of promotion readiness.

## Validation

Run python3 -m unittest discover -s tests and confirm every expected candidate container stays running, avoids OOM termination, remains inside the restart budget, and reports fresh evidence.
