# Implement Repository and Use Cases

> Version: 1.0

> Location: `graph-engineering/jobs/(next)/implement-repository-and-use-cases/JOB.md`

## Objective

The job MUST implement the real repository, mock repository, repository factory, and application use cases for a Storefront journey.

The job MUST inspect the exposed service functions in the journey's services layer (`apps/storefront/apis/<journey>/infrastructure/services/`) and wrap them into clean domain repository operations and application use cases.

The job MUST NOT modify backend database schemas, Medusa APIs, internal package SDKs, or unrelated journey domains unless explicitly requested by the user.

## Inputs

The job MUST receive:

- A kebab-case journey or domain identifier.

The job MAY receive:

- One or more specific use case identifiers to implement. When no use case identifiers are provided, the agent MUST discover and implement all service operations exposed in the journey's services layer;
- Explicit environment variable names or feature flags for mock switching (defaults to `NEXT_PUBLIC_USE_MOCK` or `USE_MOCK`).

Examples:

```txt
Implement the repository, factory, and use cases for the account journey.
```

```txt
Implement account repository, factory, and use cases for getCurrentUser and updateProfile.
```

## Scope

The agent MAY inspect:

```txt
apps/storefront/apis/<journey>/
```

The agent MAY modify:

```txt
apps/storefront/apis/<journey>/infrastructure/repository/
apps/storefront/apis/<journey>/application/use-cases/
```

The agent MUST NOT modify the following unless the user explicitly requests it:

```txt
apps/storefront/apis/<journey>/infrastructure/services/
apps/storefront/apis/<journey>/domain/contracts/
packages/
```

## Process

**1. Inspect Exposed Service Operations**

1. The agent MUST inspect the real service exported in `apps/storefront/apis/<journey>/infrastructure/services/<journey>.service.ts`.
2. The agent MUST inspect the mock service exported in `apps/storefront/apis/<journey>/infrastructure/services/<journey>.mock.service.ts`.
3. If specific use case identifiers were not provided as input, the agent MUST select all service operations exposed by `<journey>.service.ts` for implementation.
4. The agent MUST verify the parameters and return types defined in `apps/storefront/apis/<journey>/domain/contracts/<journey>.contract.ts` or corresponding UI models.

**2. Implement Repository and Mock Repository**

1. The agent MUST implement the real repository in `apps/storefront/apis/<journey>/infrastructure/repository/<journey>.repository.ts`.
2. The real repository functions MUST invoke the corresponding service functions from `<journey>.service.ts` and handle any domain delegation or error forwarding.
3. The agent MUST implement the mock repository in `apps/storefront/apis/<journey>/infrastructure/repository/<journey>.mock.repository.ts`.
4. The mock repository functions MUST invoke the corresponding mock service functions from `<journey>.mock.service.ts` or return mock data conforming to the contract.

**3. Implement Repository Factory**

1. The agent MUST implement the repository factory in `apps/storefront/apis/<journey>/infrastructure/repository/<journey>.factory.ts`.
2. The factory function (e.g. `get<Journey>Repository()`) MUST inspect feature flags or environment variables (e.g. `process.env.NEXT_PUBLIC_USE_MOCK === "true"` or `process.env.USE_MOCK === "true"`).
3. If the mock condition is truthy, the factory MUST return the mock repository instance from `<journey>.mock.repository.ts`.
4. Otherwise, the factory MUST return the real repository instance from `<journey>.repository.ts`.

**4. Implement Application Use Cases**

1. The agent MUST implement the application use cases in `apps/storefront/apis/<journey>/application/use-cases/<journey>.use-cases.ts`.
2. Each use case function MUST obtain the active repository instance by invoking the repository factory.
3. Each use case function MUST forward the call to the repository and return its result, applying any application-level orchestrations or guards if required.

**5. Validate and Report**

1. The agent MUST inspect the generated diff and verify that all TypeScript types, exports, and imports compile without errors.
2. The agent MUST verify that the factory correctly toggles between mock and real repository implementations based on the environment flag.

## Output

The job MUST produce Project Outputs in the repository and use cases directories of the targeted journey:

```txt
apps/storefront/apis/<journey>/
├── application/
│   └── use-cases/
│       └── <journey>.use-case.ts
└── infrastructure/
    └── repository/
        ├── <journey>.factory.ts
        ├── <journey>.repository.ts
        └── <journey>.mock.repository.ts
```

On successful completion, the agent MUST report:

- The implemented repository functions, factory, and use cases;
- The environment variable used for mock switching in the factory;
- File links to all created or modified code artifacts.

On failure, the agent MUST report the missing service signatures, missing inputs, or compilation errors that prevent safe implementation.

## Prompt examples

```txt
Execute the implement-repository-and-use-cases job for the account journey and implement getCurrentUser.
```

```txt
Execute the implement-repository-and-use-cases job for saved and implement all exposed service operations into repositories, factory, and use cases.
```
