# Worker 8 — Create and Publish Journey Atoms and Molecules

Durable role guide for creating the atomic and molecular building blocks required by published journey organisms.

## Responsibility and boundaries

Worker 8 owns the following sequence:

1. Identify missing atomic and molecular pieces required by the organisms published by Worker 5.
2. Create atoms without tracking, each with its component implementation and local module stylesheet.
3. Create molecules without tracking, composing shared pieces where appropriate.
4. Publish both categories through their corresponding barrels using named exports.

Worker 9 consumes this published surface to create atom and molecule Storybook stories. Story files, fixtures, analytics wiring, organism integration, and journey route work are outside Worker 8's scope unless explicitly reassigned.

## Authoritative references

- [`RULES.md`](../../../rules/RULES.md) — repository rules for shared imports, component structure, organism publication, and the required diff validation.
- [`dependency-diagram.md`](../dependency-diagram.md) — the authoritative W5 → W8 → W9 dependency and the W8A–W8D work sequence.

The dependency contract is: Worker 5 provides published organisms; Worker 8 provides published atoms and molecules; Worker 9 builds Storybook coverage from that published surface.

## Source-backed rules and durable pointers

- Atoms, molecules, and organisms **MUST** use `@shared/` utilities. A dependency outside that boundary **MUST** be migrated or replaced before publication.
- A Worker 8 atom or molecule **MUST NOT** contain tracking, analytics registries, `useTracking`, or `TrackedAction` wiring.
- Each new piece **MUST** provide a `.component.tsx` implementation and a `.module.scss` stylesheet.
- Public pieces **MUST** be reachable through their category barrel with explicit named exports. Keep the public API and exported types intentional.
- Review direct and transitive dependencies before publication; a component-local import that is valid in isolation can still pull an out-of-bound dependency.
- Search for an existing shared equivalent before adding a new piece. Do not duplicate a reusable atom or molecule only because a journey uses it first.
- Keep the change limited to the required pieces and barrels. Do not use Worker 8 as an opportunity to change organisms, journeys, analytics, or diagrams.
- The required validation command is exactly:

```powershell
git -c core.autocrlf=false -c core.whitespace=cr-at-eol diff --check
```

## Reusable implementation patterns

### Presentational atom

```tsx
import styles from './journey-label.module.scss';

export type JourneyLabelProps = {
  label: string;
};

export function JourneyLabel({ label }: JourneyLabelProps) {
  return <span className={styles.root}>{label}</span>;
}
```

### Presentational molecule composed from a shared atom

```tsx
import { JourneyLabel } from '@shared/components/atoms/journey-label';
import styles from './journey-summary.module.scss';

export type JourneySummaryProps = {
  label: string;
  title: string;
};

export function JourneySummary({ label, title }: JourneySummaryProps) {
  return (
    <section className={styles.root}>
      <JourneyLabel label={label} />
      <h2>{title}</h2>
    </section>
  );
}
```

### Named barrel exports

```ts
export { JourneyLabel } from './journey-label/journey-label.component';
export type { JourneyLabelProps } from './journey-label/journey-label.component';
```

The names and paths above are patterns, not repository-specific contracts. Match the existing folder and barrel conventions when applying them.

## Useful queries and commands

Run from the project root when investigating a candidate piece:

```powershell
# Inventory the component categories and their files
rg --files src/shared/components | rg '(atoms|molecules|organisms)'

# Find legacy and current references that may reveal a missing shared piece
rg -n 'legacy|atom|molecule|organism' src/shared/components src/journeys

# Inspect all imports in the pieces being published; review anything outside @shared
rg -n '(^|\s)from\s+["'']' src/shared/components/atoms src/shared/components/molecules

# Inspect barrel exports and spot wildcard exports
rg -n '^export (\{|type |\*)' src/shared/components/atoms src/shared/components/molecules

# Detect accidental tracking or analytics in presentational pieces
rg -n 'useTracking|TrackedAction|track|tracker|analytics|globalRegistry' src/shared/components/atoms src/shared/components/molecules

# Required final whitespace validation
git -c core.autocrlf=false -c core.whitespace=cr-at-eol diff --check
```

The import query is intentionally broad: classify each result against the `@shared/` boundary instead of relying on a fragile regular expression.

## Pitfalls

- A local export is not publication; verify that the category barrel exposes the component and any intended public type.
- Do not add tracking to make a low-level piece convenient for one organism. Tracking belongs at the appropriate consumer boundary.
- Do not import a helper, component, style, or utility from outside `@shared/`.
- Do not assume a legacy component is reusable without checking its props, styles, and transitive imports.
- Do not use wildcard exports when explicit named exports are required by the local barrel convention or could introduce collisions.
- Do not create Worker 9 stories or fixtures as a substitute for publishing the component surface.
- Do not modify `dependency-diagram.md` or another diagram to record progress.
- Do not run npm scripts unless the orchestrator explicitly authorizes them.
- Do not substitute plain `git diff --check` for the required line-ending-safe validation command.

## Handoff checklist

- [ ] Every atom and molecule needed by the published organisms has a clear path and public name.
- [ ] Each piece has `.component.tsx` and `.module.scss` files.
- [ ] Components and their transitive dependencies stay within the `@shared/` boundary.
- [ ] Atoms and molecules contain no tracking or analytics wiring.
- [ ] Category barrels expose the intended components and types through named exports.
- [ ] No duplicate, ambiguous, wildcard, or provisional exports remain.
- [ ] Organism consumers can import the pieces from the published barrels.
- [ ] Worker 9 has the exact component paths and export names needed for its stories.
- [ ] `git -c core.autocrlf=false -c core.whitespace=cr-at-eol diff --check` passes.
- [ ] No dependency diagram was modified.
