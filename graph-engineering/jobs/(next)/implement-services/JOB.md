# Implement Services

> Version: 1.1

> Location: `graph-engineering/jobs/(next)/implement-services/JOB.md`

## Objective

The job MUST implement the real and mock service functions for one Storefront journey.

The job MUST perform an end-to-end contract analysis and resolve the real source of every returned field before writing an adapter.

The job MUST NOT assume that Auth, `public` Supabase tables, Medusa, or existing analysis artifacts are interchangeable data sources.

## Inputs

The job MUST receive:

- A kebab-case journey or domain identifier;
- One or more service use cases to implement.

The job MAY receive:

- Prior use-case or DTO data-flow artifacts;
- Required UI return types or field mappings;
- Explicit source constraints, error-handling requirements, or mock data.

Examples:

```txt
Implement the getCurrentUser service for the account journey.
```

```txt
Implement account getCurrentUser and getDeliveryAddresses using the latest account journey artifacts.
```

## Scope

The agent MAY inspect:

```txt
apps/storefront/apis/<journey>/
apps/storefront/src/
packages/auth/
packages/ui/
packages/db-types/
supabase/migrations/
apps/medusa/
```

The agent MAY modify:

```txt
apps/storefront/apis/<journey>/infrastructure/services/
apps/storefront/apis/<journey>/domain/contracts/
packages/ui/src/marketplace/types/
```

The agent MUST NOT modify application callers, database migrations, Medusa code, or unrelated API domains unless the user explicitly requests it.

## Process

**1. Discover the Service Boundary**

1. The agent MUST resolve the service directory as `apps/storefront/apis/<journey>/infrastructure/services/`.
2. The agent MUST inspect the journey's existing contracts, use cases, services, mocks, and exports.
3. The agent MUST inspect relevant prior artifacts when supplied, but MUST treat them as guidance rather than proof of current implementation state.

**2. Verify Data Authority and End-to-End Contract Analysis**

1. The agent MUST inspect the package function and its return type for every package-backed use case.
2. The agent MUST perform an end-to-end contract analysis by comparing:
   - The actual backend schema and operations (e.g. Supabase `customer_addresses` table);
   - The Storefront wrappers, actions, and adapters (e.g. `listBuyerCustomerAddresses()`);
   - The model consumed by the UI (e.g. `DeliveryAddress`).
3. The agent MUST verify Storefront wrappers:
   - If a wrapper only re-exports a source function, the agent MUST record it as equivalent.
   - If a wrapper transforms results, changes errors, or applies rules, the agent MUST treat it as custom application logic and document the difference (e.g. a wrapper that returns `{ ok: false, code: ... }` on a Supabase error is not equivalent to a service that throws an exception).
4. The agent MUST inspect queried application tables, migrations, and existing readers before mapping profile, identity, address, or preference fields.
5. The agent MUST inspect Medusa code only when the requested use case requires Medusa data.
6. The agent MUST NOT map Auth provider identities to business or fiscal identities without verified semantic equivalence.

**3. Classify Fields and Define Contracts**

1. The agent MUST classify each field before writing an adapter:
   - Direct mapping (e.g. `reference_notes` → `referenceNotes`);
   - Conditional mapping (e.g. `latitude` and `longitude` → `geo` only when both exist);
   - Backend field without UI representation (e.g. `id` → `—`);
   - UI field without backend source (e.g. `—` → `mapThumbnail`);
   - Unverifiable semantics (e.g. `is_default` does NOT imply `kind: "home"`).
2. The agent MUST add or correct DTO aliases in the journey contract when a package or backend boundary needs an explicit type.
3. The agent MUST preserve external DTOs and adapt them to UI types through service-local mapping functions.
4. If the backend returns a verified field required by the use case but the UI model cannot express it, the agent MAY update the UI contract to add that field (e.g. adding `label`, `district`, `referenceNotes`, and `isDefault` to `DeliveryAddress`).
5. When a UI model shape changes, the agent MUST migrate affected consumers, including adapters, components, fixtures, and stories (e.g. replacing `location.streetAddress` and `location.extendedAddress` with `addressLine1` and `addressLine2`).
6. The agent MUST preserve nullable authentication behavior when the package can return no authenticated user.

**4. Implement Services and Document Mappings**

1. The agent MUST implement the real service in `<journey>.service.ts` using verified data sources.
2. The agent MUST implement the equivalent mock behavior in `<journey>.mock.service.ts` when the journey has a mock service.
3. Every service that adapts data between backend and UI MUST include a mandatory mapping documentation block placed immediately above the public service function performing the adaptation:

```ts
/**
 * | Backend source            | UI model field    | Mapping                                  |
 * | ------------------------- | ----------------- | ---------------------------------------- |
 * | `address_line_1`          | `addressLine1`    | Direct                                   |
 * | `address_line_2`          | `addressLine2`    | Direct when present                      |
 * | `is_default`              | `isDefault`       | Direct                                   |
 * | `latitude`, `longitude`   | `geo`             | Direct when both are present             |
 * | `id`                      | —                 | Not represented by the UI model          |
 * | —                         | `kind`            | No verified backend source               |
 * | —                         | `mapThumbnail`    | No verified backend source               |
 *
 * Storefront wrappers:
 * - Identify Storefront wrappers that add adaptation or error-handling logic.
 * 
 * Pending:
 * - Explain any temporary fallback or unresolved semantic mapping. 
 */
```

4. The agent MUST preserve explicit scope boundaries:
   - The job MAY change a UI model and its consumers when indispensable for the service to correctly represent verified data.
   - The job MUST NOT create new backend capabilities, migrations, media sources, or business rules to fill missing fields (e.g. leaving `mapThumbnail` as pending without inventing URLs or creating image tables).
5. The agent MUST NOT modify callers unless the user explicitly expands the scope.

**5. Validate and Report**

1. The agent MUST inspect the final diff and run the narrowest relevant static validation available.
2. If unrelated existing failures block validation, the agent MUST report their file and error without modifying them.
3. The agent MUST report the sources of authority used for each returned field, verified Storefront wrappers, detected wrapper-specific logic, modified files, validation results, and pending mappings.

## Output

The job MUST produce project code output in the selected journey's service and contract directories.

Output generation and formatting are executed manually by the agent.

```txt
apps/storefront/apis/<journey>/
├── domain/contracts/<journey>.contract.ts
└── infrastructure/services/
    ├── <journey>.service.ts
    └── <journey>.mock.service.ts
```

On successful completion, the agent MUST report:

- The implemented service functions and modified file links;
- The verified authority for every mapped field;
- Validation results and any pending mappings.

On failure, the agent MUST report the missing journey, use case, source-of-truth evidence, or validation error that prevents safe implementation.

## Prompt examples

```txt
Execute the implement-services job for the account journey and implement getCurrentUser.
```

```txt
Execute the implement-services job for saved and implement the requested mock and production services using the latest journey artifacts.
```
