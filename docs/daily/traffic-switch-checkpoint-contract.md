# Add traffic switch checkpoint contract

<!-- daily-pr-task: traffic-switch-checkpoint-contract -->

A blue-green traffic switch should be recoverable as a transaction. Before promotion, the checkpoint must record distinct current and candidate colors, the immutable candidate digest, a validated proxy configuration snapshot, the healthy candidate observation, and the previous upstream required for rollback. The contract is local and deterministic; the deployment runner remains responsible for persisting the checkpoint before reloading Nginx.

## Portfolio Value

Makes proxy promotion preconditions and rollback state explicit, preventing a traffic switch that cannot be safely reversed.

## Validation

Run `python3 -m unittest discover -s tests` and confirm invalid colors, mutable artifacts, unhealthy candidates, invalid proxy state, and missing rollback targets fail.
