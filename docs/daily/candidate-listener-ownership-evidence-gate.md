# Add candidate listener ownership evidence gate

<!-- daily-pr-task: candidate-listener-ownership-evidence-gate -->

Static blue/green port policy does not prove that the expected containers own the runtime listeners. This offline gate validates fresh observed listener evidence, distinct endpoints for both colors, expected Compose project ownership, running container identities, and active listening state before Nginx promotion.

## Portfolio Value

Extends port configuration safety into runtime evidence that Nginx will promote listeners owned by the intended blue-green project and containers.

## Validation

Run python3 -m unittest discover -s tests and confirm duplicate endpoints, missing colors, wrong project ownership, stopped sockets, invalid container IDs, stale observations, and invalid policy fail.
