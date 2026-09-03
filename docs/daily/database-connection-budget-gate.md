# Add database connection budget gate

<!-- daily-pr-task: database-connection-budget-gate -->

During blue-green overlap, each application color can independently exhaust a shared database even when host resources are healthy. This offline gate calculates the declared pool demand of both colors against a database connection ceiling and reserved administrative capacity. It validates configuration metadata only; it does not connect to a database.

## Portfolio Value

Adds an explicit database protection contract for the period when blue and green application pools coexist.

## Validation

Run python3 -m unittest discover -s tests and confirm both color pools must be declared, pooled, and within the usable database connection budget.
