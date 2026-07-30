# Implement Use Case Services

## Objective

The job MUST implement the service operations required by one or more use cases.

The journey identifies the service files to update. Each use case is implemented independently.

The job MUST add compatible production and mock service operations without replacing existing implementations.

## Inputs

The job MUST receive:

* One journey identifier.
* One or more use cases.

The journey identifier MUST contain lowercase words separated by hyphens.

Each use case MUST provide enough information to determine its inputs, result, behavior, and failure conditions. This information MAY come from the user, structured output from a previous job, or explicitly provided frontend source code.

Example:

```txt
Journey: cart

Use cases:
- load-cart
  Input: cart identifier
  Result: cart with its items
  Failure: cart not found
- add-cart-item
  Input: cart identifier, product identifier, quantity
  Result: updated cart
  Failure: product unavailable
```

The agent MAY inspect the project to resolve the implementation details required by the use cases.

## Required files

The following files MUST already exist for the selected journey:

```txt
apis/[journey]/infrastructure/services/
├── [journey].service.const.ts
├── [journey].mock.service.ts
└── [journey].service.ts
```

When a required file is missing, the job MUST fail and report its path.

## Process

### 1. Define the contract

For every use case, the agent MUST determine the service operation name, input type, result type, and expected errors.

The operation MUST represent backend communication or data adaptation. It MUST NOT contain use-case orchestration.

### 2. Explore the context

The agent MUST inspect only the files needed to understand:

* How the frontend requests or consumes the data.
* Existing service conventions and shared types.
* Available backend routes, handlers, SDKs, or clients.
* Backend request and response DTOs.
* Existing adapters, serializers, authentication, and error handling.

The agent MUST trace the relevant frontend-to-backend path far enough to identify the real transport contract.

The agent MUST NOT invent endpoints, DTO fields, or backend capabilities.

### 3. Plan the adaptation

Before editing, the agent MUST produce a concise plan per use case:

```txt
Use case: load-cart
Service operation: getCart
Backend operation: GET /cart
Request adaptation: none
Response adaptation: CartResponseDto -> Cart
Mock behavior: return deterministic cart data
Files: cart.service.ts, cart.mock.service.ts
```

When frontend and backend types differ, the service MUST adapt the backend DTO into the frontend-facing result type.

### 4. Implement

The agent MUST add the required operation to `[journey].service.ts` and `[journey].mock.service.ts`.

Both implementations MUST expose compatible method names, parameters, return types, and failure semantics.

The production service MUST use the existing backend integration.

The mock service MUST return deterministic data. A mutating operation MAY keep the minimum module-scoped state needed for later calls to observe the mutation.

The agent MAY add stable endpoints, keys, defaults, or fixtures to `[journey].service.const.ts`.

The agent MUST preserve unrelated exports and behavior. It MUST NOT replace complete service files or implement factories, repositories, use cases, server actions, or UI code.

## Examples

Production service with DTO adaptation:

```ts
export async function getCart(input: GetCartInput): Promise<Cart> {
  const response = await apiClient.get<CartResponseDto>(`/carts/${input.cartId}`);

  return {
    id: response.id,
    items: response.lines.map((line) => ({
      productId: line.product_id,
      quantity: line.quantity,
    })),
  };
}
```

Compatible mock service:

```ts
export async function getCart(input: GetCartInput): Promise<Cart> {
  return {
    id: input.cartId,
    items: [...mockCartItems],
  };
}
```

Several use cases MAY add several operations to the same pair of service files:

```txt
cart.service.ts
├── getCart
├── addCartItem
└── removeCartItem

cart.mock.service.ts
├── getCart
├── addCartItem
└── removeCartItem
```

## Output

The job produces project code, not a managed run artifact.

On success, the agent MUST report the use cases implemented, operations added, DTO adaptations performed, backend limitations found, and tests executed.

On failure, the agent MUST report the affected use case and the missing or unsupported dependency.

# Prompt examples

```txt
Execute the implement-use-case-services job for journey cart and these use cases:

- load-cart
- add-cart-item
```

```txt
Execute the implement-use-case-services job for journey account using the use cases returned by the previous job.
```
