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
3. When the reference section component supports a prop for nested configuration, the job MUST preserve that configuration on the equivalent organism by passing the nested component's `propsEngine` result through the supported prop. The nested component MUST NOT be rendered or commented separately. The job MUST use this pattern:

```tsx
{props.heroSection && (
    <HeroBanner
        {...HeroBanner.propsEngine(props.heroSection)}
        leadsForm={props.leadsFormModalOptions.content && LeadsFormHeroV2.propsEngine(props.leadsFormModalOptions.content)}
    />
)}
```

4. When no equivalent organism exists for a directly rendered page section component, the job MUST preserve that component's complete JSX invocation as a comment in the target page and include `/* No organism found */` as a comment block. The commented invocation MUST retain its place in the original page order and MUST include analytics imports, event callbacks, and analytics props, but the invocation MUST be fully commented.

* The job MUST apply changes only to the target page and MUST NOT modify the Pages Router reference.
* The job MUST NOT investigate, classify, or correct TypeScript errors produced by organism `propsEngine` calls, even when those errors appear in the target page during the migration.
* Any `propsEngine` type error MUST remain outside the job's scope and MUST NOT change the organism migration process or output requirements.

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

Execute migrate-page-organisms-to-app-router job.

Organism catalog: src/shared/components/organisms/index.ts
Target page: app/(landing-page)/tarjeta-de-credito/page.tsx
Pages Router reference: pages/tarjeta-de-credito-deprecated.tsx