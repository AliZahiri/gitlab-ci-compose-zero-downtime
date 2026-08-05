# Add release platform compatibility gate

<!-- daily-pr-task: release-platform-compatibility-gate -->

An immutable image can still be unusable when its operating-system or CPU architecture does not match the host running a blue-green release. This offline gate validates explicit candidate and rollback platform metadata against the configured deployment target before promotion. It consumes supplied release evidence only; it does not query a registry or mutate a host.

## Portfolio Value

Prevents a blue-green promotion from advancing an otherwise valid image that cannot run on the target Docker platform, while retaining an explicit compatible rollback artifact.

## Validation

Run `python3 -m unittest discover -s tests` and confirm matching candidate and rollback platforms pass while missing artifacts, blank image identity, OS or architecture mismatches, and invalid target policy values fail.
