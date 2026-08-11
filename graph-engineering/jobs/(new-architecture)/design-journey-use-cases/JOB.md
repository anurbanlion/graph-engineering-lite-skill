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

0. Before inspecting any source, the agent MUST reuse all relevant information already available in context and in indexes. The agent MUST NOT rediscover information that is already available.
0.1. Before classifying operations, the agent MUST inventory every relevant logical section composed by each screen associated with a supplied page. The inventory MUST retain every detected screen section.
0.2. For every supplied page, the agent MUST read each associated screen and record its sections. For each section, the agent MUST record the existing logical section component as `Section` — which MAY be the same as `Source Component(s)` — and its own component path as `Path`; when no section component exists, `Path` MUST be empty.
1. The agent MUST inspect every supplied route, server page, client shell, layout, and referenced UI screen before proposing operations. Pages MUST be treated as server components and shells as client components.
2. For each page, the agent MUST identify server functions, guards, redirects, and server-side operations. For each shell, the agent MUST identify server actions, event handlers, hooks, and navigation operations.
3. The agent MUST classify an operation as a use case when it represents a user goal, business action, data retrieval, data mutation, authentication action, or meaningful navigation action.
3.1. The agent MUST preserve the section architecture detected in the page, shell, and screen. For CMS-sourced data, the agent MUST propose one CMS call per relevant section, including routes, content, and configuration sections.
4. Guards, route context, and pure framework utilities MUST NOT be classified as use cases.
5. The agent MUST document guard, redirect, not-found, and href outcomes as Navigation Scenarios when they leave or change the current route. The agent MUST document sorting, selection controls, tab changes, and in-page scrolling as Local Scenarios unless they invoke an application boundary. When a feedback control mutates an existing persisted entity, the agent MUST classify it as the owning domain action, not as another invocation of the preceding action.
6. Hooks and state functions expressing operational intent MUST be reclassified under the relevant expected use case.
7. The agent MUST evaluate the indexes already loaded into context and the supplied implementation for a semantically compatible operation, and SHOULD extend or reuse it before proposing a new use case.
8. The agent MUST propose preliminary UI data models by inspecting the types consumed or displayed by the page and shell (e.g. `User`, `DeliveryAddress[]`, `CartItem[]`). These models represent what the journey ideally needs, independent of backend structure.

## Output

The job MUST produce a Managed Output as a Markdown document.

When the journey has a shared layout, multiple routes, or shared client state, the template MUST have an applicable `Shared Layout` section followed by one section per route. Each section MUST contain separate `Use Cases`, `Actions`, `Navigation Scenarios`, and `Local Scenarios` subsections.

The `Navigation Scenarios` and `Local Scenarios` tables MUST use BDD-inspired `When` and `Then` language. Each `Then` cell MAY contain multiple ordered consequences.

A scenario MAY have multiple equivalent triggers and triggering components when they lead to the same `Then` consequences. The template MUST record them in one scenario row rather than duplicate the scenario.

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

## Detected Sections

| Page | Section | Source Component(s) | Path | Notes |
| --- | --- | --- | --- | --- |
| `Home` | `Hero` | `HeroSection` | `packages/ui/src/.../HeroSection.tsx` | Existing logical section. |
| `Home` | `Promotions` | `PromotionsSection` | `packages/ui/src/.../PromotionsSection.tsx` | Existing logical section. |
| `Home` | `Footer` | `Footer` | `packages/ui/src/.../Footer.tsx` | Existing logical section. |
| `Home` | `NewSection` | `NewSection` | | No component yet. |

## Shared Layout (when applicable)

### Use Cases

| Kind | Type | Signature | Source | Description |
| --- | --- | --- | --- | --- |
| 🎯 Expected | Service operation | `getOwnedCart(): Promise<Cart>` | `apis/cart/...` | Returns the active cart with fulfillment options. Loaded once in layout. |

### Actions

| Kind | Type | Signature | Source | Description |
| --- | --- | --- | --- | --- |

### Navigation Scenarios

| Scenario | When | Then | Triggering Component | Description |
| --- | --- | --- | --- | --- |

### Local Scenarios

| Scenario | When | Then | Triggering Component | Description |
| --- | --- | --- | --- | --- |

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

### Navigation Scenarios

| Scenario | When | Then | Triggering Component | Description |
| --- | --- | --- | --- | --- |
| Access is denied | An authorization guard rejects the current user. | The current route ends.<br>The buyer navigates to the defined fallback route.<br>No protected screen is rendered. | `RouteGuard` | Guard outcome that changes route rendering. |

### Local Scenarios

| Scenario | When | Then | Triggering Component | Description |
| --- | --- | --- | --- | --- |
| Change sort | The user chooses a sort option. | The visible rows reorder locally.<br>No server request occurs. | `ListingSection` | Operates on already loaded rows. |
```

On successful completion, the agent MUST report the pages and shells analyzed, expected use cases, proposed UI data models, and the managed output file link.

## Prompt examples

```txt
Execute the design-journey-use-cases job using these files:

- apps/storefront/src/app/demo/[lang]/account/page.tsx
- apps/storefront/src/app/demo/[lang]/account/shell.tsx
```
