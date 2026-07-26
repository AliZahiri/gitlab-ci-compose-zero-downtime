# Add promotion resume checkpoint contract

<!-- daily-pr-task: promotion-resume-checkpoint -->

A CI runner interruption should not force operators to guess which blue/green transition completed. This checkpoint contract combines immutable candidate identity, current and candidate colors, ordered transition journal states, and rollback readiness into a resumable record. It supports deterministic recovery decisions without contacting production during validation.

## Portfolio Value

Adds deterministic interruption recovery evidence so promotion resumes only from an ordered, immutable, rollback-ready checkpoint.

## Validation

Run `python3 -m unittest discover -s tests` and confirm ordered immutable checkpoints pass while invalid colors, mutable digests, missing or skipped journal states, and absent rollback readiness fail.
