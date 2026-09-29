# Design Delivery Boundary

## Input

- The validated rule, capability assessment, current journey architecture, and relevant Marketplace UI types.

## Process

1. Classify each operation as generic server data, named browser interaction, or UI-only composition.
2. Distinguish provider DTOs from existing UI-ready models and reuse an existing model whenever it fits.
3. Define execution owner, source grouping, limits, empty and failure behavior, typed props, callbacks, and route object needs.
4. Record optional workers and parallelization decisions.

## Output

- A delivery-boundary decision, required contracts, and worker prerequisites.
