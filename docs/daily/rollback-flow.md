# Document blue-green rollback flow

<!-- daily-pr-task: rollback-flow -->

Rollback should reuse the same blue/green switch path as deployment. The previous color stays available until the new color is promoted and verified.

Rollback checklist:

- identify last known healthy color
- confirm old container is still present or restartable
- switch reverse proxy upstream back to the previous color
- verify health endpoint through the public proxy
- only then stop the failed color

## Portfolio Value

Makes the zero-downtime Docker Compose story more credible by covering failure recovery.

## Validation

Review the markdown file and confirm rollback depends on health checks, not manual guessing.
