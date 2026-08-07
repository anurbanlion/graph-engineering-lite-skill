# Implement Journey Services

## Objective

The job MUST implement the real and mock service functions for a Storefront journey.

The job MUST adapt backend DTOs to UI domain models using the field mappings documented in the Blueprint.

## Inputs

The job MUST receive:

- A kebab-case journey identifier.

The job MUST have the Blueprint artifact and the generated `[journey].contract.ts` available in context or in the workspace.

The job MAY receive specific use case identifiers. When none are provided, the agent MUST implement services for all use cases with contracts defined in `[journey].contract.ts`.

## Scope

The agent MAY inspect:

```txt
apps/storefront/apis/<journey>/
packages/
```

The agent MAY modify:

```txt
apps/storefront/apis/<journey>/infrastructure/services/<journey>.service.ts
apps/storefront/apis/<journey>/infrastructure/services/<journey>.mock.service.ts
apps/storefront/apis/<journey>/infrastructure/services/<journey>.service.const.ts
```

## Process

1. The agent MUST inspect the journey contracts and the Blueprint's Field Mapping Specifications.
2. The agent MUST verify data authority by inspecting the actual backend functions, Supabase queries, or Medusa endpoints that serve each field.
3. The agent MUST implement the real service in `<journey>.service.ts` calling verified backend sources.
4. The agent MUST implement the mock service in `<journey>.mock.service.ts` returning mock data that conforms to the contract.
5. Every service function that adapts backend data to a UI model MUST include a mandatory mapping documentation block (JSDoc table) immediately above the function:

```ts
/**
 * | Backend source          | UI model field  | Mapping                    |
 * | ----------------------- | --------------- | -------------------------- |
 * | `auth.user.email`       | `email`         | Direct                     |
 * | `user_profiles.phone`   | `phone`         | Direct when present        |
 * | —                       | `mapThumbnail`  | No verified backend source |
 */
```

6. The agent MUST NOT create new backend capabilities, migrations, or media sources to fill missing fields.

## Output

The job MUST produce Project Output:

```txt
apps/storefront/apis/<journey>/infrastructure/services/
├── <journey>.service.ts
├── <journey>.mock.service.ts
└── <journey>.service.const.ts
```

On successful completion, the agent MUST report the implemented service functions, verified sources of authority, modified file links, and any pending mappings.

## Prompt examples

```txt
Execute the implement-journey-services job for the account journey.
```
