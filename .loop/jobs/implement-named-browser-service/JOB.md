# Implement Named Browser Service

## Input

- The named-operation decision, target rule, capability assessment, and delivery model.

## Process

1. Implement the browser-safe named service at `infrastructure/services/<named-service>.service.ts`.
2. Put only provider DTOs in the journey contract and map them to the existing delivery model.
3. Do not import server-only modules, privileged clients, Server Actions, generic server services, or service barrels.
4. Do not create its factory, use case, route composition, hook, or mock in this job.

## Output

- One browser-safe named service, provider DTOs, and a mapping to the existing delivery model.
