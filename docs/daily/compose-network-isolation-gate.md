# Add Compose network isolation gate

<!-- daily-pr-task: compose-network-isolation-gate -->

A blue-green Compose deployment should expose traffic through the reverse proxy instead of publishing application or data-service ports directly. This offline gate validates a public/private network boundary: proxy services join both networks, workloads join only the private network, data services remain private without published ports, and every service has a declared role and network set.

## Portfolio Value

Makes the reverse proxy a real deployment boundary by preventing blue, green, and stateful services from bypassing controlled traffic switching through host-published ports.

## Validation

Run `python3 -m unittest discover -s tests` and confirm a dual-homed proxy with private workloads passes while missing networks, duplicate networks, invalid roles, public workloads, published application/data ports, absent roles, and invalid policy values fail.
