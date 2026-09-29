# Compose Marketplace UI Sources

## Input

- The target rule, UI delivery contract, and existing Marketplace components.

## Process

1. Model independent sources as separate object fields, such as `popular`, `recent`, and `autocomplete`.
2. Pass source groups through component props without flattening them in routes or demo shells.
3. Let the Marketplace UI component choose its presentation mode, rows, empty state, callbacks, and typed `routes` object.
4. Do not import Storefront infrastructure, repositories, services, or use cases into `packages/ui`.

## Output

- A source-group UI prop contract and Marketplace UI behavior for the rule's presentation states.
