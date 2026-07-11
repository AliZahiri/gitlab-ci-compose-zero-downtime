# Add deployment freeze window guard

<!-- daily-pr-task: deployment-freeze-window -->

Production deployment automation should be able to respect freeze windows during incident response, high-traffic events, or maintenance restrictions. The guard should be explicit so the pipeline can fail early before starting containers or switching traffic.

Guard inputs:

- current UTC hour
- blocked deployment hours
- emergency override flag
- clear reason when deployment is blocked

## Portfolio Value

Adds a realistic release-safety control for production deployment windows.

## Validation

Run `python3 -m unittest discover -s tests` and confirm frozen hours block deployment unless override is explicit.
