# Add deployment cancellation safety evidence gate

<!-- daily-pr-task: deployment-cancellation-safety-evidence-gate -->

Cancelling a deployment is a state transition, not a safe terminal state by itself. This offline gate requires cancellation evidence to record whether traffic switched, the resulting rollback or candidate-cleanup outcome, active-color health, transition-journal persistence, and lock release so an interrupted run cannot abandon ambiguous traffic ownership.

## Portfolio Value

Extends blue/green recovery semantics to operator and CI cancellation paths, making traffic ownership, rollback completion, durable state, and lock cleanup explicit instead of assuming process termination is safe.

## Validation

Run python3 -m unittest discover -s tests and confirm pre-switch cleanup and completed rollback pass while ambiguous traffic state, invalid outcomes, naive timestamps, unhealthy active color, missing journal evidence, and unreleased locks fail.
