# Implement Journey Repositories

## Objective

The job MUST implement the real repository, mock repository, and repository factory for a Storefront journey.

This is a structural delegation layer: repositories forward calls to services, and the factory selects between real and mock based on an environment variable.

## Inputs

The job MUST receive:

- A kebab-case journey identifier.

The job MUST have the journey services (`<journey>.service.ts` and `<journey>.mock.service.ts`) implemented in the workspace.

The job MAY receive an explicit environment variable name for mock switching (defaults to `NEXT_PUBLIC_USE_MOCK`).

## Process

1. The agent MUST inspect the exported functions from `<journey>.service.ts` and `<journey>.mock.service.ts`.
2. The agent MUST implement the real repository in `<journey>.repository.ts`, where each function delegates to the corresponding real service function.
3. The agent MUST implement the mock repository in `<journey>.mock.repository.ts`, where each function delegates to the corresponding mock service function.
4. The agent MUST implement the factory in `<journey>.factory.ts` exporting a function (e.g. `get<Journey>Repository()`) that returns the mock repository when `process.env.NEXT_PUBLIC_USE_MOCK === "true"` and the real repository otherwise.
5. Both repositories MUST expose the same interface.

## Output

The job MUST produce Project Output:

```txt
apps/storefront/apis/<journey>/infrastructure/repository/
├── <journey>.repository.ts
├── <journey>.mock.repository.ts
└── <journey>.factory.ts
```

On successful completion, the agent MUST report the implemented repository functions, the environment variable used for mock switching, and modified file links.

## Prompt examples

```txt
Execute the implement-journey-repositories job for the account journey.
```
