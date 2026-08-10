# Design Journey Use Cases

## Objective

The job MUST identify the application operations and preliminary data models required by a journey's UI.

The job MUST classify operations visible in every supplied route, layout, and shell into expected use cases, existing implementations, and excluded framework primitives.

The job MUST propose preliminary UI data models based on the data consumed or displayed by the journey screens.

## Inputs

The job MUST receive:

- A kebab-case journey identifier;
- At least one of: page and shell file paths, source code, screenshot, or user description.

When a supplied input names a sibling route, layout, or UI screen, it MUST be treated as in-scope evidence.

The job MAY receive:

- Reflection feedback from a previous audit iteration recommending model splits, use case decompositions, or data source reassignments. When present, the agent MUST incorporate the feedback to refine the use cases and UI data models accordingly.

Examples:

```txt
Page: apps/storefront/src/app/demo/[lang]/account/page.tsx
Shell: apps/storefront/src/app/demo/[lang]/account/shell.tsx
```

## Process

1. The agent MUST inspect every supplied route, server page, client shell, layout, and referenced UI screen before proposing operations. Pages MUST be treated as server components and shells as client components.
2. For each page, the agent MUST identify server functions, guards, redirects, and server-side operations. For each shell, the agent MUST identify server actions, event handlers, hooks, and navigation operations.
3. The agent MUST classify an operation as a use case when it represents a user goal, business action, data retrieval, data mutation, authentication action, or meaningful navigation action.
4. Guards, route context, and pure framework utilities MUST NOT be classified as use cases.
5. The agent MUST classify route navigation and local draft updates as framework/local behavior unless they invoke an application boundary. When a journey has transient shared state, the agent MUST document the state owner, lifetime, reset behavior, and persistence boundary.
6. Hooks and state functions expressing operational intent MUST be reclassified under the relevant expected use case.
7. The agent MUST evaluate the indexes already loaded into context and the supplied implementation for a semantically compatible operation, and SHOULD extend or reuse it before proposing a new use case.
8. The agent MUST propose preliminary UI data models by inspecting the types consumed or displayed by the page and shell (e.g. `User`, `DeliveryAddress[]`, `CartItem[]`). These models represent what the journey ideally needs, independent of backend structure.

## Output

The job MUST produce a Managed Output as a Markdown document.

When the journey has a shared layout, multiple routes, or shared client state, the template MUST have an applicable `Shared Layout` section followed by one section per route. Each section MUST contain separate `Use Cases`, `Actions`, and `Local State / Exclusions` subsections. A single-page journey MUST use only its route section without inventing a shared-layout section.

For transient journey-state models only, the Preliminary UI Data Models table MUST include `Owner`, `Lifetime`, and `Persistence` columns. `Owner` identifies the component or provider controlling the state; `Lifetime` states when it survives or resets; `Persistence` states whether and where it is stored. Backend-sourced models (e.g. `Cart`, `DeliveryAddress`) do not need these columns.

```md
## Preliminary UI Data Models

| Model | Fields | Notes |
| --- | --- | --- |
| `User` | `name`, `email`, `phone`, `avatarUrl` | Consumed by the profile display and edit form. |
| `DeliveryAddress` | `addressLine1`, `city`, `geo` | Rendered as address cards. |

| Model | Fields | Owner | Lifetime | Persistence | Notes |
| --- | --- | --- | --- | --- | --- |
| `CheckoutDraft` | `personalInfo`, `selectedAddress`, `paymentMethod` | `CheckoutProvider` | Survives sibling navigation; resets on hard refresh | Client memory only; MUST NOT persist to backend | Transient state for multi-step checkout flow. |

## Shared Layout (when applicable)

### Use Cases

| Kind | Type | Signature | Source | Description |
| --- | --- | --- | --- | --- |
| 🎯 Expected | Service operation | `getOwnedCart(): Promise<Cart>` | `apis/cart/...` | Returns the active cart with fulfillment options. Loaded once in layout. |

### Actions

| Kind | Type | Signature | Source | Description |
| --- | --- | --- | --- | --- |

### Local State / Exclusions

| Type | Signature | Source | Description |
| --- | --- | --- | --- |

## Route: `personal`

### Use Cases

| Kind | Type | Signature | Source | Description |
| --- | --- | --- | --- | --- |
| 🎯 Expected | Service operation | `getCurrentUser(): Promise<User>` | `apis/account/infrastructure/services/account.service.ts` | Returns the authenticated user. |
| 🔎 Existing | Server function | `getCurrentUser()` | `@/lib/demo/server-db` | Current function called by the page. |

### Actions

| Kind | Type | Signature | Source | Description |
| --- | --- | --- | --- | --- |
| 🎯 Expected | Application action | `logout(): Promise<void>` | `To be defined` | Ends the session. |
| 🔎 Existing | Server action | `logoutAction()` | `../actions` | Current action invoked by the shell. |

### Local State / Exclusions

The following are not considered use cases:

| Type | Signature | Source | Description |
| --- | --- | --- | --- |
| Guard | `assertUser(user)` | `@/lib/demo/utils` | Validates access. |
| Local draft update | `setPersonalInfo(data)` | `CheckoutProvider` | Updates transient provider state. |
```

On successful completion, the agent MUST report the pages and shells analyzed, expected use cases, proposed UI data models, and the managed output file link.

## Prompt examples

```txt
Execute the design-journey-use-cases job using these files:

- apps/storefront/src/app/demo/[lang]/account/page.tsx
- apps/storefront/src/app/demo/[lang]/account/shell.tsx
```
