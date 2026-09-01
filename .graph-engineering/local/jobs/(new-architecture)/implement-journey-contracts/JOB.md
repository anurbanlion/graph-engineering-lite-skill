# Implement Journey Contracts

## Objective

The job MUST generate or update the TypeScript contract file (`[journey].contract.ts`) with the backend response DTOs required by the selected use cases.

The job MUST update UI model types when the Blueprint recommends changes to align with backend boundaries.

## Inputs

The job MUST receive:

- A kebab-case journey identifier;
- One or more use case identifiers to implement. When no identifiers are provided, the agent MUST offer the user the full list of use cases from the Blueprint and ask for selection before proceeding.

The job MUST have the Blueprint artifact available in context.

## Scope

The agent MAY modify:

```txt
apps/storefront/apis/<journey>/domain/contracts/<journey>.contract.ts
packages/ui/src/marketplace/types/
```

## Process

1. The agent MUST read the Blueprint's Five-Layer Discovery Matrix and Field Mapping Specifications for the selected use cases.
2. The agent MUST inspect relevant backend sources (Supabase schemas, Package SDK types, Medusa route responses) to derive exact DTO shapes.
3. The agent MUST define DTOs using `export type` with structured JSDoc metadata (`@sourceType`, `@operation`, `@caller`, `@backendSource`, `@usedBy`).
4. If a compatible DTO already exists in the contract file, the agent MUST reuse it and append the new use case to its `@usedBy` tag.
5. When the Blueprint recommends UI model changes (e.g. adding `isDefault` to `DeliveryAddress`), the agent MUST apply those changes to the UI type definitions and migrate affected consumers.

## Output

The job MUST produce Project Output:

```txt
apps/storefront/apis/<journey>/domain/contracts/<journey>.contract.ts
```

On successful completion, the agent MUST report the DTOs added or reused, UI model changes applied, and modified file links.

## Prompt examples

```txt
Execute the implement-journey-contracts job for the account journey and use cases getCurrentUser and getDeliveryAddresses.
```

```txt
Execute the implement-journey-contracts job for the account journey.
```
