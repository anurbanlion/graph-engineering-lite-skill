# Compose Generic Journey Application Boundary

## Input

- The generic production and mock services, target journey, and delivery boundary contract.

## Process

1. Create or update production and mock repositories under `infrastructure/repository`.
2. Create or update the repository factory in that same directory; select mock or production there.
3. Create or update the generic use case. It creates the repository factory and may be exported from the journey use-case barrel.
4. Keep generic server operations out of Client Components and named operations out of these barrels.

## Output

- Repository, mock repository, repository factory, generic use case, and an appropriate generic barrel export.
