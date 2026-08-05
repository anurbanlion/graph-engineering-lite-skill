# Analyze Journey Use Cases

## Objective

The job MUST analyze a page and its shell to identify the application operations represented by their server-side functions, server actions, event handlers, navigation behavior, and hooks.

The job MUST distinguish the expected application or service operation from the implementation currently used by the page or shell.

The job MUST NOT treat framework utilities, local state primitives, route context, guards, or navigation APIs as use cases by themselves.

## Inputs

The job MUST receive at least one of the following:

- page and shell file paths;
- page and shell source code;
- additional source code;
- screenshot or design reference;
- user description of the screen or flow.

The job MAY receive naming, architecture, or output constraints.

Examples:

```txt
Page: apps/storefront/src/app/demo/[lang]/account/page.tsx
Shell: apps/storefront/src/app/demo/[lang]/account/shell.tsx
```

```txt
Analyze the account page and shell from the supplied screenshot and description.
```

## Process

**1. Inspect supplied evidence**

1. The agent MUST inspect only the inputs supplied to the job.
2. The agent MUST analyze source code only when it is included in the supplied inputs.
3. The page MUST be treated as a server component and the shell MUST be treated as a client component.
4. The agent MUST NOT open, resolve, inspect, or trace imported files.
5. The agent MUST NOT infer internal implementation details beyond the supplied evidence.

**2. Identify existing operations**

1. For the page, the agent MUST identify referenced or invoked server functions, guards, redirects, and other server-side operations.
2. For the shell, the agent MUST identify referenced or invoked server actions, event handlers, hooks, route utilities, and navigation operations.
3. For every identified operation, the agent MUST record its visible signature when it can be derived from the supplied source. When parameter or return types are unavailable, the signature MUST use only the information visible in the supplied input.
4. The agent MUST record the import source or `Not yet implemented` when no implementation exists.

**3. Classify use cases**

1. The agent MUST classify an operation as a use case when it represents a user goal, business action, data retrieval, data mutation, authentication action, or meaningful navigation action in the journey.
2. The agent MUST reclassify as use cases all hooks and state functions that express an operational intent, even if they are currently poorly designed or named.
3. A state hook that expresses operational intent MUST be classified under the relevant expected use case. For example, `useState(user)` supporting profile edits MUST be listed as existing implementation of `updateProfile`, not as a generic UI-state exclusion.
4. Data retrieval or mutation that crosses an integration boundary SHOULD produce an expected service operation.
5. An expected service operation MUST return the frontend domain model required by the journey rather than a transport DTO.
6. Guards such as access assertions (such as `assertUser`) MUST NOT be classified as use cases unless they represent an explicit user-facing business operation, and MUST remain as explicit exceptions under "The following functions are not considered use cases:".
7. Purely contextual or infrastructure elements (such as `routeContext` or `useParams<{ lang: string }>()`) MUST NOT be classified as use cases because they do not represent a relevant user operation.
8. Generic state or framework usage with no reasonably identifiable application operation MUST be listed as not considered a use case.

**4. Define expected operations**

1. Each classified use case MUST have one `🎯 Expected` row describing the operation that should exist in the target architecture.
2. Each current implementation that supports that use case MUST have a corresponding `🔎 Existing` row immediately after its expected row.
3. Framework hooks, state initialization, setters, and route utilities that implement a meaningful operation MUST be grouped as existing implementation rows directly beneath that operation's expected row. They MUST NOT appear as independent excluded operations.
4. Expected and existing identifiers MUST preserve appropriate TypeScript naming and MUST NOT be converted to kebab-case.
5. Expected operation identifiers MUST use the journey's concise domain vocabulary. For direct navigation, use the action name exposed to the journey when evident from the source, such as `back(): void`, rather than invented wrapper names such as `navigateBack(): void`.
6. Expected service operations SHOULD use the journey service path:

```txt
apis/<journey>/infrastructure/services/<journey>.service.ts
```

7. Expected server actions, application actions, or navigation actions MAY use another appropriate target path or `To be defined` when the supplied evidence is insufficient.
8. When no current implementation exists, the expected row MUST use `Not yet implemented` in the Source column.
9. The agent MUST use concise descriptions that explain the user or application outcome rather than restating the function name.

**5. Validate the analysis**

1. The agent MUST preserve separate `Page Use Cases` and `Shell Use Cases` sections.
2. Every expected row MUST describe a meaningful operation rather than a framework primitive.
3. Every existing row MUST be supported by the supplied inputs.
4. Guards and other meaningful exclusions SHOULD remain visible beneath the corresponding page or shell section. Pure framework utilities, route context, and implementation dependencies MUST NOT be listed separately when they only support an identified use case.
5. The agent MUST NOT include operations that cannot be identified or reasonably inferred from the supplied inputs.

## Output

The job MUST produce a Managed Output as a Markdown document.

Output generation and formatting are performed manually by the agent from the supplied evidence.

The agent MUST count table delimiters before finalizing the output. A table with `N` header columns MUST contain `N` separator cells and `N` cells in every data row.

The output MUST preserve the following structure:

```md
## Page Use Cases

| Kind | Type | Signature | Source | Description |
| --- | --- | --- | --- | --- |
| 🎯 Expected | Service operation | `getCurrentUser(): Promise<User>` | `apis/account/infrastructure/services/account.service.ts` | Returns the authenticated user required by the account journey. |
| 🔎 Existing | Server function | `getCurrentUser()` | `@/lib/demo/server-db` | Current function called directly by the page. |
| 🎯 Expected | Service operation | `getDeliveryAddresses(): Promise<DeliveryAddress[]>` | `apis/account/infrastructure/services/account.service.ts` | Returns the current user's delivery addresses. |
| 🔎 Existing | Server function | `getDeliveryAddresses()` | `@/lib/demo/server-db` | Current function called directly by the page. |

The following functions are not considered use cases:

| Type | Signature | Source | Description |
| --- | --- | --- | --- |
| Guard | `assertUser(user)` | `@/lib/demo/utils` | Validates access to the account route. |

## Shell Use Cases

| Kind | Type | Signature | Source | Description |
| --- | --- | --- | --- | --- |
| 🎯 Expected | Application action | `logout(): Promise<void>` | `To be defined` | Ends the authenticated session. |
| 🔎 Existing | Server action | `logoutAction()` | `../actions` | Current action invoked by the shell. |
| 🎯 Expected | Service operation | `updateProfile(input: UpdateProfileInput): Promise<User>` | `apis/account/infrastructure/services/account.service.ts` | Persists edited account details and returns the updated user. |
| 🔎 Existing | UI state | `useState(...)` | `react` | Current local state holds editable account details, but no mutation operation is visible. |
| 🎯 Expected | Navigation action | `back(): void` | `To be defined` | Returns the user from the account screen. |
| 🔎 Existing | Navigation | `router.back()` | `next/navigation` | Current navigation performed by the shell. |

The following functions are not considered use cases:

| Type | Signature | Source | Description |
| --- | --- | --- | --- |
| Route context | `useParams()` | `next/navigation` | Reads the current language route parameter. |
```

The `Kind` column MUST contain only `🎯 Expected` or `🔎 Existing`.

The `Type` column MUST describe the architectural or current implementation role, such as `Service operation`, `Application action`, `Navigation action`, `Server function`, `Server action`, `UI state`, `Guard`, or `Route context`.

`Not yet implemented` MUST appear only in the Source column.

On successful completion, the agent MUST report:

- the page and shell analyzed;
- the expected use case operations identified;
- the existing implementations associated with them;
- the operations explicitly excluded from use-case classification;
- the managed output file link.

On failure, the agent MUST report the missing input, unsupported evidence, or output-generation error.

## Prompt examples

```txt
Execute the analyze-journey-use-cases job using these files:

- apps/storefront/src/app/demo/[lang]/account/page.tsx
- apps/storefront/src/app/demo/[lang]/account/shell.tsx
```

```txt
Execute the analyze-journey-use-cases job for the cart journey using the supplied screenshot and flow description.
```