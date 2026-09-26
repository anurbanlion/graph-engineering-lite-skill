# Worker 1 — Organism Contract

## Responsibility

Worker 1 owns the organism contract phase. For each assigned organism, review the directly relevant legacy data shape and create or correct its `.props.ts` with exported public prop aliases and a backend-only `propsEngine`. This contract is the prerequisite for Worker 2 (fixtures and Storybook) and Worker 3 (flat organism implementation).

## Authoritative References

- `.loop/orchestration/guidelines-migration/dependency-diagram.md`: W1A is legacy-component review; W1B is `.props.ts`, props, and `propsEngine` creation.
- `.loop/rules/RULES.md`: required organism layout, shared-only dependencies, and the mandatory whitespace validation.
- The assigned legacy page and component: authoritative sources for section slug, prop semantics, ordering, and mapping behavior.
- `src/core/types/contentful.d.ts`: authoritative source for V2 Contentful field shapes and nullability.

## Durable Rules

- W1 is a persistent worker identity for the organism-contract responsibility. It is not scoped to a Gantt time unit or a specific organism.
- Preserve user edits and leave legacy sources unchanged; they are reference-only.
- Limit W1 changes to the assigned organism's `.props.ts`. Components, styles, fixtures, stories, analytics, barrels, route integration, and reports belong to other workers.
- Export public prop types and independently useful nested aliases. Inline one-use nested data shapes when the contract requires it.
- `propsEngine` maps supplied backend data only. It returns `{}` for a missing section and MUST NOT create mock content.
- Normalize nullish Contentful values to `undefined` when the public prop uses optional fields.
- When public props use `IoImage`, map V2 assets to the public `{ url, alt }` shape instead of exposing nullable backend fields.
- Use PowerShell syntax for repository commands. Do not run npm scripts unless explicitly authorized.

## Reusable Contract Patterns

```ts
export type ExampleProps = {
  title?: string;
};

export function propsEngine(section?: Maybe<IoLiquidSectionV2>): ExampleProps {
  if (!section) return {};

  return {
    title: section.title ?? undefined,
  };
}
```

```ts
const items = (section.sections ?? [])
  .filter((item): item is IoLiquidSectionV2 => item?.contentType === "landingIoLiquidSection")
  .map((item) => ({
    title: item.title ?? undefined,
  }));
```

## Useful Queries and Commands

```powershell
rg -n -C 8 'ComponentName|component-name' 'pages/legacy-page.tsx' 'components' -g '*.ts' -g '*.tsx'
Get-Content -Raw 'src/core/types/contentful.d.ts'
git -c core.autocrlf=false -c core.whitespace=cr-at-eol diff --check
```

For a focused tracked-file inspection:

```powershell
git diff -- 'src/shared/components/organisms/<organism>/<organism>.props.ts'
git diff --cached -- 'src/shared/components/organisms/<organism>/<organism>.props.ts'
```

## Pitfalls

- Do not use plain `git diff --check`; the repository requires the command above to avoid CRLF-related false whitespace reports.
- Untracked files do not appear in `git diff`; inspect them explicitly before handoff.
- Do not derive a new contract from a similarly named organism. Derive it from the assigned legacy component and direct backend types.
- Do not introduce analytics callbacks in the initial contract unless the assigned W1 task explicitly requires them; analytics is normally Worker 4 work.
- Treat optional slug values deliberately when a contract normalizes or matches category data.

## Handoff Guidance

- Confirm the assigned legacy source and relevant section shape were reviewed.
- Confirm only the assigned `.props.ts` changed.
- Confirm public props and independently reusable aliases are exported.
- Confirm `propsEngine` has no mock data, preserves source ordering, and returns `{}` for a missing section.
- Run `git -c core.autocrlf=false -c core.whitespace=cr-at-eol diff --check`.
- Return a concise completion message to the orchestrator.
