# Migrate Page Organisms to App Router

> Version: 1.0

## Objective

The job MUST replace legacy components in the target App Router page with equivalent existing organisms after identifying the available organism implementations and confirming any selected Pages Router reference.

The job MUST NOT create new organisms, refactor or improve existing organisms internally, or include analytics tags.

## Inputs

The job MUST receive:

- file paths for an index or catalog of available organisms; and
- a target app router page path.

The job MAY receive:

- a previous Pages Router reference.

Examples:

```txt
Organism catalog: src/shared/components/organisms/index.ts
Target page: app/(landing-page)/nuestra-app/page.tsx
Pages Router reference: pages/nuestra-app-deprecated.tsx
```

## Scope

The agent MUST inspect the supplied organism catalog, the target page, the supplied previous Pages Router reference, and candidate files within `pages/` if no reference is supplied.

The agent MUST not inspect organisms implementation.

The agent MAY modify the target page.

The agent MUST NOT modify the Pages Router reference, shared organism implementations, Analytics tags, or unrelated routes unless the user explicitly requests it.

## Process

### Preparation

1. The job MUST read the catalog of available organisms.
2. When no previous Pages Router reference is available, the job MUST search for a candidate within `pages/` and ask the user to confirm it before using it as the Pages Router reference.
3. The job MUST review the previous Pages Router reference after the user supplies or confirms it.

### Organism Migration

1. For each component within the Pages Router reference, the job MUST search the catalog for an equivalent organism.
2. When an equivalent organism exists, the job MUST replace the legacy component in the target page using the organism's `propsEngine` mechanism, preserve applicable `mt-*` classes in `className`, and add conditional rendering when the corresponding data may be absent.
3. When no equivalent organism exists, the job MUST preserve the original implementation as a comment in the target page and add the comment `/* No organism found */` to make the missing organism explicit.

- The job MUST apply changes only to the target page and MUST NOT modify the Pages Router reference.

## Output

The job MUST produce Project Output consisting of the target page modified with the migrated organisms defined by the completed job process. Every successful completion MUST produce the skill-defined Context Output.

Output generation and page migration are executed manually by the agent.

**Code / Directory Structure Output**

```txt
<target-page-path>
```

On failure, the agent MUST report the unavailable organism catalog, missing target page, unavailable Pages Router reference, or unconfirmed candidate.

## Prompt examples

```txt
Execute migrate-page-organisms-to-app-router job.

Organism catalog: src/shared/components/organisms/index.ts
Target page: app/(landing-page)/nuestra-app/page.tsx
Pages Router reference: pages/nuestra-app-deprecated.tsx
```

```txt
Execute migrate-page-organisms-to-app-router job.

Organism catalog: src/shared/components/organisms/index.ts
Target page: app/(landing-page)/nuestra-app/page.tsx
```

```txt
Execute migrate-page-organisms-to-app-router with src/shared/components/organisms/index.ts and app/(landing-page)/nuestra-app/page.tsx.
```

```txt
Migrate organisms to app/(landing-page)/nuestra-app/page.tsx using src/shared/components/organisms/index.ts and pages/nuestra-app.tsx as the Pages Router reference.
```
