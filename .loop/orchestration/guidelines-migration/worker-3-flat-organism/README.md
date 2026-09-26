# Worker 3 — Flat Organism

## Responsibility

Worker 3 owns the visual implementation of migrated organisms. For each assigned organism, W3:

1. Inspects the direct legacy reference for composition and behavior.
2. Reviews the published shared atoms, molecules, and organisms before creating UI.
3. Implements or corrects the organism `.component.tsx` using existing shared pieces.
4. Implements or corrects the scoped `.module.scss`.
5. Creates or corrects the local `index.ts` that exposes the component, props type, and `propsEngine`.

W3 must not modify the props contract, fixtures, Storybook, analytics, global publication, routes, or legacy sources unless an assignment explicitly expands that scope.

## Authoritative references

- Worker ownership and prerequisites: `.loop/orchestration/guidelines-migration/dependency-diagram.md`
- Repository rules: `.loop/rules/RULES.md`
- Component conventions: `openspec/specs/components-conventions/design.md`
- Organism source: `src/shared/components/organisms/<organism>/`
- Shared reuse indexes:
  - `src/shared/components/atoms/index.ts`
  - `src/shared/components/molecules/index.ts`
  - `src/shared/components/organisms/index.ts`

## Flat-organism patterns

### Local index

```ts
import { ComponentName as Component } from "./component-name.component";
import { propsEngine } from "./component-name.props";

export type { ComponentNameProps } from "./component-name.props";

export const ComponentName = Object.assign(Component, { propsEngine });
```

### Imports and composition

- Use a `const` declaration for organisms.
- Use configured absolute aliases for nonlocal imports. The stylesheet is the local exception: `./component-name.module.scss`.
- Reuse published components through `@shared`; do not import implementation from legacy `components/` paths.
- Keep simple presentational regions inline. Do not create internal components unless they have their own logic, state, mapping, or reusable responsibility.
- Use `&&` for a single optional render region.

### Scoped layout

```scss
@use "/app/styles" as *;

.organism {
  @include screen-max-width(grid);
}
```

- Apply `screen-max-width(grid)` when the organism needs a centered, constrained screen-level layout.
- Keep responsive media queries at stylesheet root level.
- Keep shared/base properties before responsive overrides and remove selectors made unused by a correction.

## Durable implementation guidance

- Treat legacy components as parity references only; do not edit them.
- If an appropriate shared piece is absent, do not import its legacy equivalent. Escalate it for the atom/molecule publication flow.
- For a horizontally centered flex parent at desktop, a child row that must span its content area needs `width: 100%`; use flexible cards (`flex: 1 1 0; min-width: 0`) rather than rigid minimum widths when the row must not overflow.
- Related visual regions must share the same horizontal inset at every breakpoint. For example, a category bar and its corresponding content list need matching `padding-inline` values.
- Purple dashed bounds in Storybook can be the Measure overlay rather than component CSS; inspect component styles and story parameters before changing layout.

## Useful queries and commands

```powershell
rg -l "ComponentName" components src -g '*.{tsx,ts,scss}'
Get-Content -Raw 'src/shared/components/organisms/<organism>/<organism>.props.ts'
Get-Content -Raw 'src/shared/components/organisms/<organism>/<organism>.fixtures.ts'
git -c core.autocrlf=false -c core.whitespace=cr-at-eol diff --check
```

Do not run npm scripts unless explicitly authorized.

## Pitfalls

- Do not change the legacy route or component.
- Do not extend W3 work into analytics, contracts, fixtures, stories, global indexes, or journey integration without explicit scope.
- Do not duplicate a published atom or molecule.
- Do not use a plain `git diff --check`: use the CRLF-safe validation command above.
- Do not mistake Storybook tool overlays for an implementation defect.

## Handoff checklist

- [ ] The direct legacy reference and relevant shared barrels were inspected.
- [ ] Only W3-authorized files changed.
- [ ] The existing props contract is consumed without modification.
- [ ] Optional single regions use `&&`.
- [ ] Nonlocal imports use permitted aliases and the stylesheet import is local.
- [ ] Responsive rules are root-level and unused styles were removed.
- [ ] The local index follows the `Object.assign(Component, { propsEngine })` pattern when it is in scope.
- [ ] `git -c core.autocrlf=false -c core.whitespace=cr-at-eol diff --check` passed.
