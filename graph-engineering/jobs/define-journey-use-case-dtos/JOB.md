# Define Journey Use Case DTOs

## Objective

The job MUST define the backend-facing DTOs required by one or more use cases in a journey.

The job MUST derive DTOs from backend resources and capabilities that actually exist in Medusa, Supabase, or another established backend source.

The job MUST NOT implement frontend services, repositories, use cases, actions, pages, or components.

## Inputs

The job MUST receive:

- one journey identifier;
- one or more use case identifiers.

Each identifier MUST contain lowercase words separated by hyphens.

The agent MUST discover the backend operations, resource shapes, DTO boundaries, and source locations required by the selected use cases. The agent MUST also inspect relevant existing frontend implementations to identify whether and how they already call those backend capabilities, including the clients, operations, request values, and response shapes currently consumed. Frontend evidence MUST inform the analysis but MUST NOT override the actual backend contract.

The job MAY receive explicit backend paths, modules, routes, schemas, or implementation constraints.

Examples:

```txt
Journey: account
Use cases:
- get-current-user
```

```txt
Journey: cart
Use cases:
- get-cart
- add-cart-item
```

## Scope

The agent MAY inspect backend and integration sources required to determine the available data contract, including Medusa routes, modules, SDK usage, handlers, workflows, Supabase queries, database types, and existing adapters.

The agent MAY inspect relevant frontend services, clients, actions, hooks, use cases, pages, or components only to identify existing backend calls and the request or response shapes they currently use.

The agent MAY inspect existing journey contracts to preserve compatible definitions and avoid duplication.

The agent MAY modify only:

```txt
apis/[journey]/domain/contracts/[journey].contract.ts
```

The agent MUST NOT modify the following unless the user explicitly requests it:

```txt
apis/[journey]/application/
apis/[journey]/infrastructure/
app/
components/
```

## Process

**1. Resolve backend capabilities**

1. The agent MUST inspect Medusa first for every selected use case.
2. When Medusa does not expose all required information, the agent MUST inspect established Supabase or project backend sources.
3. The agent MUST identify the concrete operation, query, route, module, or resource that supplies each required field.
4. The agent MUST inspect relevant existing frontend implementations to identify current backend calls, clients, request values, and consumed response shapes.
5. Frontend evidence MAY reveal existing integration assumptions or reusable shapes, but the agent MUST validate them against the backend source before defining DTOs.
6. The agent MUST NOT invent backend fields, relations, operations, or guarantees.

**2. Define DTO boundaries**

1. The agent MUST determine the request and response DTOs required by each use case.
2. DTO names MUST represent backend resources or transport structures rather than mechanically mirroring use case names.
3. One use case MAY require multiple DTOs, and one DTO MAY support multiple use cases.
4. DTOs MUST preserve backend nullability, optionality, identifiers, nested resources, and collection shapes unless an explicit normalization boundary is required.
5. The agent MUST reuse compatible existing DTOs instead of creating equivalent duplicates.

**3. Write journey contracts**

1. The agent MUST add or complete the required DTO definitions in `apis/[journey]/domain/contracts/[journey].contract.ts`.
2. The agent MUST preserve unrelated existing exports and contract definitions.
3. Each added DTO SHOULD include concise source traceability identifying the backend capability from which it was derived and the use cases that require it.
4. Source traceability MUST remain stable and MUST NOT depend on transient line numbers.

Example:

```ts
/**
 * Source: Medusa Store Cart API
 * Used by: get-cart, add-cart-item
 */
export interface CartDto {
  id: string;
  items: CartItemDto[];
}
```

**4. Validate contracts**

1. The agent MUST verify that every selected use case is supported by the DTOs added or reused.
2. The agent MUST verify that each field is traceable to an existing backend source.
3. The agent MUST verify that the contract file remains syntactically valid and preserves existing exports.
4. When a required backend capability does not exist, the agent MUST stop and report the affected use case and missing data source instead of fabricating a DTO.

## Output

The job MUST produce a Project Output in:

```txt
apis/[journey]/domain/contracts/
└── [journey].contract.ts
```

Output generation and formatting are performed manually by the agent from inspected backend sources.

The contract file MAY contain multiple request, response, resource, nested, pagination, or error DTOs when required by the selected use cases.

On successful completion, the agent MUST report:

- the journey and use cases analyzed;
- the DTOs added or reused;
- the Medusa, Supabase, or backend sources used;
- any relevant frontend calls or consumed response shapes found;
- any backend limitations or unresolved fields;
- the modified contract file.

On failure, the agent MUST report the affected use case, missing backend capability, invalid journey contract path, or unsupported source.

## Prompt examples

```txt
Execute the define-journey-use-case-dtos job for journey account and use case get-current-user.
```

```txt
Execute the define-journey-use-case-dtos job for journey cart and these use cases:

- get-cart
- add-cart-item
- remove-cart-item
```
