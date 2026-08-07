# Design Journey Use Cases

## Objective

The job MUST identify the application operations and preliminary data models required by a journey's UI.

The job MUST classify operations visible in the page and shell into expected use cases, existing implementations, and excluded framework primitives.

The job MUST propose preliminary UI data models based on the data consumed or displayed by the journey screens.

## Inputs

The job MUST receive:

- A kebab-case journey identifier;
- At least one of: page and shell file paths, source code, screenshot, or user description.

The job MAY receive:

- Reflection feedback from a previous audit iteration recommending model splits, use case decompositions, or data source reassignments. When present, the agent MUST incorporate the feedback to refine the use cases and UI data models accordingly.

Examples:

```txt
Page: apps/storefront/src/app/demo/[lang]/account/page.tsx
Shell: apps/storefront/src/app/demo/[lang]/account/shell.tsx
```

## Process

1. The agent MUST inspect only the supplied inputs. The page MUST be treated as a server component and the shell as a client component.
2. For the page, the agent MUST identify server functions, guards, redirects, and server-side operations. For the shell, the agent MUST identify server actions, event handlers, hooks, and navigation operations.
3. The agent MUST classify an operation as a use case when it represents a user goal, business action, data retrieval, data mutation, authentication action, or meaningful navigation action.
4. Guards, route context, and pure framework utilities MUST NOT be classified as use cases.
5. Hooks and state functions expressing operational intent MUST be reclassified under the relevant expected use case.
6. The agent MUST propose preliminary UI data models by inspecting the types consumed or displayed by the page and shell (e.g. `User`, `DeliveryAddress[]`, `CartItem[]`). These models represent what the journey ideally needs, independent of backend structure.

## Output

The job MUST produce a Managed Output as a Markdown document.

```md
## Preliminary UI Data Models

| Model | Fields | Notes |
| --- | --- | --- |
| `User` | `name`, `email`, `phone`, `avatarUrl` | Consumed by the profile display and edit form. |
| `DeliveryAddress` | `addressLine1`, `city`, `geo` | Rendered as address cards. |

## Page Use Cases

| Kind | Type | Signature | Source | Description |
| --- | --- | --- | --- | --- |
| 🎯 Expected | Service operation | `getCurrentUser(): Promise<User>` | `apis/account/infrastructure/services/account.service.ts` | Returns the authenticated user. |
| 🔎 Existing | Server function | `getCurrentUser()` | `@/lib/demo/server-db` | Current function called by the page. |

The following functions are not considered use cases:

| Type | Signature | Source | Description |
| --- | --- | --- | --- |
| Guard | `assertUser(user)` | `@/lib/demo/utils` | Validates access. |

## Shell Use Cases

| Kind | Type | Signature | Source | Description |
| --- | --- | --- | --- | --- |
| 🎯 Expected | Application action | `logout(): Promise<void>` | `To be defined` | Ends the session. |
| 🔎 Existing | Server action | `logoutAction()` | `../actions` | Current action invoked by the shell. |
```

On successful completion, the agent MUST report the page and shell analyzed, expected use cases, proposed UI data models, and the managed output file link.

## Prompt examples

```txt
Execute the design-journey-use-cases job using these files:

- apps/storefront/src/app/demo/[lang]/account/page.tsx
- apps/storefront/src/app/demo/[lang]/account/shell.tsx
```
