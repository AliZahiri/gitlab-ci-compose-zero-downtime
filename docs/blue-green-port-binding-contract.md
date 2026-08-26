# Blue-green port binding contract

During a Compose blue/green deployment, both application colors need to run concurrently while Nginx owns the public listener. Binding either candidate directly to a non-loopback host can bypass the proxy, while reusing a host port prevents both colors from coexisting.

`compose_zero_downtime.blue_green_port_binding` validates an offline deployment plan. It requires exactly one blue and one green binding, valid and distinct host ports, and IPv4 or IPv6 loopback addresses. It does not inspect Docker or claim that the planned ports are currently free.

Run the focused contract tests with:

```bash
python3 -m unittest tests.test_blue_green_port_binding
```

Use the contract before starting the candidate color, then keep the existing health, Nginx validation, promotion, and rollback gates in the deployment path.
