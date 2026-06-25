# Add rollback window guard

<!-- daily-pr-task: rollback-window-guard -->

A blue/green release should keep the previous color available until smoke checks and a minimum observation window pass. This turns rollback from an idea into an executable path.

Guard inputs:

- smoke test duration
- observation window
- stop-old-container flag
- minimum rollback window

## Portfolio Value

Shows that old containers are retained long enough to make rollback practical.

## Validation

Run the unit test and confirm short rollback windows are rejected.
