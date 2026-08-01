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

## Process

**1. Resolve backend capabilities**

1. The agent MUST inspect Medusa first for every selected use case.
2. When Medusa does not expose all required information, the agent MUST inspect established Supabase or project backend sources.
3. The agent MUST identify the concrete operation, query, route, module, or resource that supplies each required field.
4. The agent MUST inspect relevant existing frontend implementations to identify current backend calls, clients, request values, and consumed response shapes.
5. Frontend evidence MAY reveal existing integration assumptions or reusable shapes, but the agent MUST validate them against the backend source before defining DTOs.
6. The agent MUST NOT present unsupported fields, relations, operations, or guarantees as capabilities already provided by the backend.

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
5. Fields required by the use case but not currently returned by any backend source MUST be optional and MUST include a comment stating that no current backend capability provides them.

Example:

```ts
/**
 * Source: Medusa Store Cart API
 * Used by: get-cart, add-cart-item
 */
export interface CartDto {
  id: string;
  items: CartItemDto[];

  /** No current backend capability returns this field. */
  estimatedDeliveryDate?: string;
}
```

**4. Validate contracts**

1. The agent MUST verify that every selected use case is represented by the DTOs added or reused.
2. The agent MUST verify that each field is either traceable to an existing backend source or explicitly marked as an optional field not currently provided by the backend.
3. The agent MUST verify that the contract file remains syntactically valid and preserves existing exports.
4. When a required backend capability does not exist, the agent MUST propose the missing DTO or fields, mark unsupported fields as optional, and document that no current backend source returns them.

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
- any proposed optional fields not currently provided by the backend;
- the modified contract file.

On failure, the agent MUST report the affected use case, invalid journey contract path, or unsupported source inspection.

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
