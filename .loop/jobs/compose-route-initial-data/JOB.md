# Compose Route Initial Data

## Input

- The generic journey use case, typed return model, target Demo page/layout, and target rule.

## Process

1. Call generic server use cases from the server page or layout using existing composition patterns.
2. Fetch independent initial data in parallel where possible.
3. Pass returned data through typed Demo props. Do not flatten sources or choose presentation modes here.
4. Do not put initial server-data fetching in a Client Component hook or create an API route solely to relay it.

## Output

- Server-composed initial data and typed route-to-client Demo props.
