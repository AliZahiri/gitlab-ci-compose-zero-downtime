# Add deployment audit event policy

<!-- daily-pr-task: deploy-audit-event-policy -->

Deployment audit events should capture who deployed what, where, and with what result. This keeps blue/green promotion traceable after incidents.

Required fields:

- actor
- commit sha
- image
- target color
- result

## Portfolio Value

Shows deployment events are auditable with actor, target, and result metadata.

## Validation

Run the unit test and confirm audit events require actor, commit, image, and result.
