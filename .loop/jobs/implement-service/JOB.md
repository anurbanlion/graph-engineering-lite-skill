# Implement Generic Journey Service

## Input

- The target rule, capability assessment, delivery boundary contract, and backend semantics when required.

## Process

1. Implement only the generic production operation in `apps/storefront/apis/<journey>/infrastructure/services/<journey>.service.ts`.
2. Keep server-only dependencies here only when W3 assigned a server boundary. Do not import this graph from Client Components or named browser operations.
3. Put provider DTOs in `domain/contracts/<journey>.contract.ts`. Reuse existing delivery models; do not rename a model as a DTO or duplicate it.
4. Map only rule-required fields, limits, empty states, and failures. Update the capability map with the selected source and limitations.

## Output

- One generic production service, provider DTOs, mapping to the existing delivery model, and an updated capability map.
