# Analyze Journey Use Cases

## Objective

The job MUST analyze a page and its shell to identify the use cases represented by server-side functions, server actions, and hooks.

## Inputs

At least one of the following inputs MUST be provided:

* Page and shell file paths.
* Page and shell source code.
* Additional source code.
* Screenshot or design reference.
* User description of the screen or flow.

The user description MAY be refined through a short back-and-forth conversation.

If no input is available, the agent MUST ask the user for at least one input before continuing.

## Process

1. The agent MUST read only the provided inputs.
2. The agent MUST analyze source code only when it is included in the provided inputs.
3. When source code is available, the agent MUST identify:
   * Server-side functions referenced or invoked by the page.
   * Server actions and hooks referenced or invoked by the shell.
4. When source code is unavailable or insufficient, the agent MUST infer the required server-side functions, server actions, and hooks from the screenshot, design reference, or user description.
5. The agent MUST assign a proposed identifier to every inferred item.
6. Proposed identifiers MUST end with `UseCase`. Exceptions:
    * hooks
    * back
7. Proposed hook identifiers MUST begin with `use`.
8. The agent MUST organize all identified or inferred items according to the required output format.

The agent MUST NOT open, resolve, inspect, or trace imported files.

The agent MUST NOT infer internal implementation details beyond the provided inputs.

The page MUST be treated as a server component.

The shell MUST be treated as a client component.

## Output

The output MUST be a Markdown document with aligned table columns using whitespaces and the following sections.

When the implementation exists, the output SHOULD follow this format:

```md
## Page Use Cases

| Use Case             | Server Function | Source           |
| -------------------- | --------------- | ---------------- |
| Load the user list   | `getUsers`      | `@/server/users` |
| Load available roles | `getRoles`      | `@/server/roles` |

## Shell Use Cases

| Use Case                         | Type          | Server Action or Hook | Source            |
| -------------------------------- | ------------- | --------------------- | ----------------- |
| Create a user                    | Server action | `createUser`          | `@/actions/users` |
| Delete a user                    | Server action | `deleteUser`          | `@/actions/users` |
| Manage search state              | Hook          | `useState`            | `react`           |
| Synchronize filters with the URL | Hook          | `useQueryState`       | `nuqs`            |
```

When the implementation is unavailable, the output SHOULD follow this format:

```md
## Page Use Cases

| Use Case         | Server Function            | Source              |
| ---------------- | -------------------------- | ------------------- |
| Load saved items | `loadSavedItemsUseCase`    | Not yet implemented |

## Shell Use Cases

| Use Case                    | Type          | Server Action or Hook          | Source              |
| --------------------------- | ------------- | ------------------------------ | ------------------- |
| Add a saved item to the cart| Server action | `addSavedItemToCartUseCase`    | Not yet implemented |
| Go back                     | Hook          | `useGoBackUseCase`             | Not yet implemented |
```

`Not yet implemented` MUST appear only in the `Source` column.

The server function, server action, or hook column MUST always contain an existing or proposed identifier.

The agent SHOULD use concise, user-oriented descriptions for each use case.

The agent MUST NOT include use cases that cannot be identified or reasonably inferred from the provided inputs.

# Prompt examples

```txt
Using the job-graph-engineering local skill (.codex/skills), execute the 

- analyze-page-shell-use-cases 

job using these files:

- apps/storefront/src/app/demo/[lang]/account/cart/page.tsx
- apps/storefront/src/app/demo/[lang]/account/cart/shell.tsx
```

```txt
Using the job-graph-engineering local skill (.codex/skills), execute the 

- analyze-page-shell-use-cases 

job using these files:

- apps/storefront/src/app/demo/[lang]/page.tsx
- apps/storefront/src/app/demo/[lang]/shell.tsx

for run: home-page

and these:

- apps/storefront/src/app/demo/[lang]/account/page.tsx
- apps/storefront/src/app/demo/[lang]/account/shell.tsx

for run: account-page

These are two jobs
```