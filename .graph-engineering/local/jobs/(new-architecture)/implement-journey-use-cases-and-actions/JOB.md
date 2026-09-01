# Implement Journey Use Cases and Actions

## Objective

The job MUST implement the application use cases and Next.js Server Actions for a Storefront journey.

Use cases MUST obtain the active repository via the factory and forward calls.

Actions MUST provide the entry point for UI mutations with error handling, validation, and cache revalidation as required by the Blueprint.

## Inputs

The job MUST receive:

- A kebab-case journey identifier.

The job MUST have the Blueprint artifact and the repository factory (`<journey>.factory.ts`) available in the workspace.

## Process

**1. Implement Use Cases**

1. The agent MUST implement use case functions in `<journey>.use-case.ts`.
2. Each use case function MUST obtain the repository instance by calling the factory function.
3. Each use case function MUST forward the call to the repository and return its result.

**2. Implement Actions**

1. The agent MUST implement Server Actions in `<journey>.action.ts` using `"use server"` directive.
2. Each action MUST call the corresponding use case function.
3. Actions that perform mutations MUST include error handling (`try/catch`), returning structured results (e.g. `{ ok: boolean; error?: string }`).
4. When the Blueprint's discovery matrix reveals existing error-handling patterns (e.g. toast notifications, redirects on auth failure), the agent MUST preserve or replicate those patterns.
5. Actions MAY include `revalidatePath` or `revalidateTag` calls when cache invalidation is required after a mutation.
6. The agent MUST preserve local provider actions as client-side functions when the Blueprint classifies them as local; it MUST NOT turn them into Server Actions.

**3. Define Public Export Boundary**

1. The agent MUST explicitly export runtime APIs from `application/use-cases/index.ts` and `application/actions/index.ts`.

**4. Register in Central Discovery Inventories**

1. The agent MUST add explicit named imports for the new use case functions to `apps/storefront/apis/use-cases.index.ts`.
2. The agent MUST add explicit named imports for the new action functions to `apps/storefront/apis/actions.index.ts`.
3. Each import statement MUST include a brief inline comment with the format `// Reuse <functionName> when <brief usage hint>`.
4. Imports MUST be grouped by journey, with each journey group separated by a blank line.

## Output

The job MUST produce Project Output:

```txt
apps/storefront/apis/<journey>/application/
├── use-cases/
│   ├── index.ts
│   └── <journey>.use-case.ts
└── actions/
    ├── index.ts
    └── <journey>.action.ts

apps/storefront/apis/use-cases.index.ts
apps/storefront/apis/actions.index.ts
```

On successful completion, the agent MUST report the implemented use cases, the implemented Server Actions with their error-handling and cache-invalidation strategy, local provider actions preserved (if any), index file updates, and modified file links.

## Prompt examples

```txt
Execute the implement-journey-use-cases-and-actions job for the account journey.
```
