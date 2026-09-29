# Implement Service Mock

## Input

- The target rule, delivery contract, selected operation class, and journey mock conventions.

## Process

1. Implement deterministic mock data in the matching mock service.
2. Match the production delivery model, limits, empty state, and observable failures.
3. Do not alter repositories, factories, use cases, routes, hooks, or UI.

## Output

- A deterministic mock service compatible with the delivery contract.
