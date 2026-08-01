# Implement Use Case Services

## Objective

The job MUST implement the production and mock service operations required by one or more use cases within a journey.

The job MUST preserve existing service behavior and MUST NOT implement use-case orchestration, factories, repositories, server actions, or UI code.

## Inputs

The job MUST receive:

- one kebab-case journey identifier;
- one or more kebab-case use case identifiers.

The job MAY receive:

- explicit project constraints or source paths supplied by the user.

The agent MUST discover the service inputs, result types, failure conditions, backend capabilities, and required adaptations from the workspace.

Examples:

```txt
Journey: cart
Use cases:
- load-cart
- add-cart-item
```

```txt
Journey: account
Use cases:
- get-current-user
```

## Scope

The following files MUST already exist for the selected journey:

```txt
apis/<journey>/infrastructure/services/
├── <journey>.service.const.ts
├── <journey>.mock.service.ts
└── <journey>.service.ts
```

The agent MAY inspect the frontend and backend files required to identify existing usages, implementations, transport contracts, DTOs, adapters, authentication, and error handling.

The agent MAY modify:

```txt
apis/<journey>/infrastructure/services/<journey>.service.const.ts
apis/<journey>/infrastructure/services/<journey>.mock.service.ts
apis/<journey>/infrastructure/services/<journey>.service.ts
```

The agent MUST NOT modify the following unless the user explicitly requests it:

```txt
apis/<journey>/application/factories/
apis/<journey>/application/repositories/
apis/<journey>/application/use-cases/
apis/<journey>/infrastructure/actions/
app/
components/
```

When a required service file is missing, the job MUST fail and report its path.

## Process

**1. Explore the use case context**

1. The agent MUST locate how each requested use case is consumed by the frontend.
2. The agent MUST inspect related service, mock, action, client, SDK, route, handler, DTO, adapter, authentication, and error-handling code.
3. The agent MUST inspect the relevant Medusa implementation when it is the source of the backend contract.
4. The agent MUST identify all relevant existing implementations, including production, mock, partial, duplicated, and journey-specific variants.
5. The agent MUST NOT select an implementation solely because it appears more complete.
6. The agent MUST NOT invent endpoints, DTO fields, backend capabilities, or unsupported behavior.

**2. Define the service contract**

1. For each use case, the agent MUST determine the production service operation and the compatible mock operation.
2. The agent MUST determine each operation's parameters, result type, failure semantics, and data adaptation requirements.
3. The service operation MUST represent backend communication, persistence, or data adaptation and MUST NOT contain use-case orchestration.
4. When frontend and backend types differ, the service MUST adapt backend DTOs into the frontend-facing result type.

The agent MUST prepare a concise implementation plan for each use case:

```txt
Use case: load-cart
Production operation: getCart
Mock operation: getCart
Backend source: GET /store/carts/:id
Request adaptation: GetCartInput -> route parameters
Response adaptation: StoreCartResponseDto -> Cart
Mock behavior: return deterministic cart state
Files: cart.service.ts, cart.mock.service.ts
```

**3. Implement the operations**

1. The agent MUST add or complete the required operation in `<journey>.service.ts` using existing backend integrations and project conventions.
2. The agent MUST add or complete the compatible operation in `<journey>.mock.service.ts`.
3. Production and mock operations MUST expose compatible names, parameters, result types, and failure semantics.
4. A mutating mock operation MUST preserve the minimum module-scoped state required for later calls in the same runtime to observe the mutation.
5. The agent MAY add stable endpoints, keys, defaults, or fixtures to `<journey>.service.const.ts`.
6. The agent MUST preserve unrelated exports, implementations, and behavior.
7. The agent MUST NOT replace complete service files when a focused additive change is sufficient.

**4. Validate the result**

1. The agent MUST verify that every requested use case has compatible production and mock operations.
2. The agent MUST verify that DTO adaptations match the discovered backend and frontend contracts.
3. The agent MUST run focused existing tests or validation commands when the project provides an established convention.
4. The agent MUST report backend limitations or unsupported operations rather than fabricating an implementation.

## Output

The job MUST produce a Project Output by modifying the selected journey service files:

```txt
apis/<journey>/infrastructure/services/
├── <journey>.service.const.ts
├── <journey>.mock.service.ts
└── <journey>.service.ts
```

Output generation and validation are executed manually by the agent using the discovered project contracts.

On successful completion, the agent MUST report:

- the journey and use cases processed;
- the production and mock operations added or completed;
- the DTO adaptations and backend sources used;
- the modified files and validation results;
- any backend limitations or deferred behavior.

On failure, the agent MUST report the affected use case, missing service file, unsupported backend capability, or invalid project contract.

## Prompt examples

```txt
Execute the implement-use-case-services job for journey cart and the load-cart and add-cart-item use cases.
```

```txt
Execute the implement-use-case-services job for journey account and the get-current-user use case.
```