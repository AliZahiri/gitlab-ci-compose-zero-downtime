# Add blue-green proxy cache bypass contract gate

<!-- daily-pr-task: blue-green-proxy-cache-bypass-contract-gate -->

A proxy cache can serve an old colour after traffic promotion unless release-sensitive paths have an explicit bypass or cache-key separation strategy. This offline gate checks declared promotion paths and a deliberate cache strategy; it does not alter Nginx or send traffic.

## Portfolio Value

Makes cache behavior an explicit promotion safety concern, reducing the risk of serving stale-colour responses after a switch.

## Validation

Run python3 -m unittest discover -s tests and confirm only an approved strategy with unique absolute promotion paths passes.
