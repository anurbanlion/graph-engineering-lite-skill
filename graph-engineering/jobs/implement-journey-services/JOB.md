# Implement Journey Services

## Objective

The job MUST implement or refactor the service layer for one or more journeys.

For every selected journey, the job MUST produce a production service and a mock service that follow the current project architecture and support the journey use cases.

The job MUST adapt existing implementations when they do not follow the required architecture.

The job MUST preserve externally observable behavior unless the provided requirements explicitly change it.

## Inputs

The job MUST receive one or more journey identifiers.

Each journey identifier MUST contain one or more lowercase words separated by hyphens.

The job MUST also receive enough use-case information to determine the operations required from each journey service.

Use-case information MAY be provided by:

* The user.
* Structured output returned by a previously executed job.
* Explicitly provided use-case files or source code.

The job MAY receive additional project constraints, including:

* Existing backend endpoints or server functions.
* Available SDKs, clients, adapters, or transport libraries.
* Authentication, authorization, caching, error-handling, or persistence requirements.
* Existing service interfaces, conventions, tests, or examples that MUST remain compatible.

When the required use cases or project constraints are unavailable, the agent MUST ask for the missing input before implementing code.

## Required files

For every journey, the following files MUST already exist:

```txt
apis/[journey]/infrastructure/services/[journey].service.const.ts
apis/[journey]/infrastructure/services/[journey].mock.service.ts
apis/[journey]/infrastructure/services/[journey].service.ts
```

The agent MUST NOT create missing architecture files manually.

When a required file is missing, the job MUST fail and report the missing path. A graph MAY execute `scaffold-journey-architecture` before this job to ensure the required structure exists.

## Process

1. The agent MUST identify the selected journeys and their required use cases from the provided inputs.
2. The agent MUST inspect the three required service files for each selected journey.
3. The agent MAY inspect only the additional project files required to understand existing service conventions, available backend capabilities, shared types, clients, tests, or compatibility constraints.
4. Before editing code, the agent MUST prepare a concise implementation plan that maps each required use case to:
   * The production service operation.
   * The mock service behavior and persisted in-memory state, when required.
   * The constants, keys, endpoints, delays, or configuration shared by the service implementations.
   * Any current backend limitation or project constraint that affects the implementation.
5. The agent MUST implement or refactor `[journey].service.ts` as the production-facing service.
6. The production service MUST use the backend capabilities, SDKs, clients, adapters, and conventions currently available in the project.
7. The production service MUST NOT invent backend endpoints, server functions, response fields, or unsupported capabilities.
8. When a required operation is not supported by the current backend, the agent MUST preserve a clear service boundary and represent the limitation explicitly rather than fabricating an implementation.
9. The agent MUST implement or refactor `[journey].mock.service.ts` as a deterministic local substitute for the production service.
10. The mock service MUST expose behavior compatible with the production service contract.
11. When a mock operation changes data, the mock service MUST maintain the minimum in-memory state required for subsequent operations in the same runtime to observe that change.
12. Mock state MUST be scoped to the journey service module unless the provided project architecture defines another explicit persistence mechanism.
13. The agent MUST implement or refactor `[journey].service.const.ts` only for constants shared by the production or mock service, including stable keys, defaults, configuration values, or mock fixtures.
14. The constants file MUST NOT contain service orchestration or mutable runtime state.
15. The agent MUST reuse existing project types when they are available and appropriate.
16. The agent MUST keep production and mock service method names, parameters, return types, and error semantics compatible.
17. The agent MUST update relevant existing tests when needed and MUST add focused tests when the project already has an established testing convention for the service layer.
18. The agent MUST NOT implement repositories, factories, use cases, server actions, UI components, or unrelated infrastructure as part of this job.
19. The agent MUST NOT perform broad cleanup or refactoring outside the selected journey services.
20. The agent MUST review the completed changes against every provided use case and project constraint.

## Output

The job produces project code rather than a managed run artifact.

For every selected journey, the completed output MUST include:

```txt
apis/
└── [journey]/
    └── infrastructure/
        └── services/
            ├── [journey].service.const.ts
            ├── [journey].mock.service.ts
            └── [journey].service.ts
```

Existing service files MAY be modified or replaced when required to conform to the architecture and provided use cases.

The production service and mock service MUST provide compatible contracts.

The mock service MUST behave deterministically and MUST persist required state for the lifetime of its module instance.

When execution succeeds, the agent MUST report:

* Journeys processed.
* Service files created, implemented, or refactored.
* Use cases covered.
* Backend limitations or deferred operations.
* Tests executed and their results, when applicable.

When execution fails, the agent MUST report the reason and the affected journey or file.

# Prompt examples

```txt
Execute the implement-journey-services job for these journeys:

- cart
- saved

Use the provided journey use cases and the current backend clients.
```

```txt
Execute the implement-journey-services job for account using the use cases returned by the previous job.

Refactor the existing production and mock services to follow the current journey service architecture.
```
