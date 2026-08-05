# Implement Services

> Version: 1.0

> Location: `graph-engineering/jobs/implement-services/JOB.md`

## Objective

The job MUST implement the real and mock service functions for one Storefront journey.

The job MUST resolve the real source of every returned field before writing an adapter.

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

**2. Verify Data Authority**

1. The agent MUST inspect the package function and its return type for every package-backed use case.
2. The agent MUST inspect Storefront wrappers and re-exports of each source function to determine whether they add application logic.
3. The agent MUST treat a Storefront wrapper that only re-exports a source function as equivalent to that source and record the verification in the implemented service comment or final report.
4. The agent MUST alert the user and report the added behavior when a Storefront wrapper contains application logic; the agent MUST NOT treat that wrapper as equivalent to its source without explicit user direction.
5. The agent MUST inspect the queried application tables, migrations, and existing readers before mapping profile, identity, address, or preference fields.
6. The agent MUST inspect Medusa code only when the requested use case requires Medusa data.
7. The agent MUST record unresolved fields as explicit implementation assumptions or pending work.
8. The agent MUST NOT map Auth provider identities to business or fiscal identities without verified semantic equivalence.

**3. Define Contracts and Adapters**

1. The agent MUST add or correct DTO aliases in the journey contract when a package or backend boundary needs an explicit type.
2. The agent MUST preserve external DTOs and adapt them to UI types through service-local mapping functions.
3. The agent MUST avoid changing UI types unless the requested service cannot represent a verified required field without the change.
4. The agent MUST preserve nullable authentication behavior when the package can return no authenticated user.

**4. Implement Services**

1. The agent MUST implement the real service in `<journey>.service.ts` using the verified data sources.
2. The agent MUST implement the equivalent mock behavior in `<journey>.mock.service.ts` when the journey has a mock service.
3. The agent MUST add a concise comment above an incomplete public service function identifying verified pending mappings or assumptions.
4. The agent MUST NOT modify callers unless the user explicitly expands the scope.

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
