# Enable Backend Capability

## Input

- The capability assessment, delivery-boundary decision, existing backend evidence, and target rule.

## Process

1. Verify whether the selected capability already satisfies the rule.
2. Implement backend behavior only when access, validation, or response semantics are missing.
3. Preserve the provider contract; do not implement Storefront UI wiring.

## Output

- Reused or implemented backend behavior and documented access, request, response, empty, and failure semantics.
