# Add Compose project namespace contract gate

<!-- daily-pr-task: compose-project-namespace-contract-gate -->

Concurrent blue-green stacks should not collide through reused Compose project or resource names. This offline gate derives an expected project namespace from stack and environment slugs, validates observed resource identities, and requires every non-shared container, network, or volume to remain inside that namespace. Explicitly shared resources must be separately approved.

## Portfolio Value

Prevents cross-environment Compose resource collisions and makes intentional shared infrastructure explicit before blue-green promotion.

## Validation

Run python3 -m unittest discover -s tests and confirm invalid slugs, mismatched project names, unnamespaced resources, duplicate identities, and unapproved shared resources fail.
