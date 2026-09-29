# Compose Named Browser Use Case

## Input

- The named browser service, matching mock when required, target rule, and delivery boundary contract.

## Process

1. Create the named factory at `infrastructure/repository/<named-service>.factory.ts`.
2. Create `application/use-cases/<named-service>.use-case.ts`; its exported function creates the factory inside the function.
3. Select production or mock behavior in the named factory when both exist. Keep the entire graph browser-safe.
4. Do not export named services, factories, or use cases through barrels. Consumers import the named use case by direct file path.

## Output

- A named factory in `infrastructure/repository`, a direct named browser use case, and no server-only dependency in the browser graph.
