# Worker 5 — Organism Publication

## Responsibility

Worker 5 publishes a completed shared organism. Its authoritative dependency-diagram responsibilities are:

1. Export the organism from `src/shared/components/organisms/index.ts`.
2. Verify the public index and component-scoped TypeScript state.
3. Correct only errors caused by, or specific to, the target organism.

Worker 5 MUST NOT implement the base organism, create a journey, modify legacy sources, or fix unrelated repository errors. It works only after the contract, fixtures/Storybook, implementation, and analytics prerequisites are ready.

## Authoritative references

- [Dependency diagram](../dependency-diagram.md): W5 ownership and prerequisite flow.
- [Global Loop rules](../../../../rules/RULES.md): shared-component conventions and required whitespace validation.
- [Component conventions](../../../../openspec/specs/components-conventions/design.md): index and barrel conventions. Read this as reference only; never invoke an OpenSpec workflow.
- [Analytics documentation](../../../../analytics/docs/): consult only when public types or production caller configuration involve analytics.

The standard component and analytics jobs are useful reference material, but publication ownership remains W5A–W5C in the dependency diagram. Report, review, and self-improve jobs are not part of this migration's W5 workflow.

## Publication pattern

The local index MUST attach `propsEngine` and export the public props type:

```ts
import { OrganismName as _Component } from "./organism-name.component";
import { propsEngine } from "./organism-name.props";

export type { OrganismNameProps } from "./organism-name.props";

export const OrganismName = Object.assign(_Component, { propsEngine });
```

The global organism barrel MUST use an explicit named export, its props type, and a concise reuse comment:

```ts
// Reuse this organism when a landing section needs <capability>.
export { OrganismName, type OrganismNameProps } from "./organism-name";
```

For organisms built before local-index creation became part of flat-organism ownership, add the local index only when the orchestrator explicitly authorizes that transitional exception.

## Durable rules

- The dependency diagram is the source of truth for ownership; a Gantt time unit is only a scheduling boundary.
- Preserve edits observed between turns. Do not revert another worker's or the user's changes to simplify publication.
- Publish only the named target organism. Do not expand a type-check result into unrelated cleanup.
- Navbar, PreFooterBanner, and Footer are already published organisms; route-shell integration does not enter the W5 organism-publication flow.
- Use project absolute aliases for component imports; same-directory style imports remain relative.

## Useful queries and commands

```powershell
rg -n 'OrganismName|<OrganismName' src app --glob '!**/*.stories.*'
Get-Content -Raw 'src/shared/components/organisms/<organism>/index.ts'
Get-Content -Raw 'src/shared/components/organisms/index.ts'
& '.\node_modules\.bin\tsc.cmd' --noEmit --pretty false
git -c core.autocrlf=false -c core.whitespace=cr-at-eol diff --check
```

The direct local TypeScript command is not an npm script. When it is required, distinguish target-organism errors from existing generated `.next` failures and leave unrelated failures untouched.

## Pitfalls

- Do not create a new W5 for each Gantt unit; reuse the persistent worker identity.
- Do not run npm scripts.
- Do not modify legacy sources, routes, analytics schemas, or another organism while publishing one target.
- Always run exactly `git -c core.autocrlf=false -c core.whitespace=cr-at-eol diff --check`; plain `git diff --check` produces avoidable CRLF warnings in this workspace.
- Untracked files do not appear in ordinary `git diff`; inspect them directly and use `git status --short` when necessary.

## Handoff checklist

- [ ] W1 contract and `propsEngine` are ready.
- [ ] W2 fixtures and Storybook stories are ready.
- [ ] W3 component, SCSS, and local index are ready, unless an explicit transitional exception is supplied.
- [ ] W4 analytics prerequisites are ready for perceptible interactions.
- [ ] The local index exports props and attaches `propsEngine` with `Object.assign`.
- [ ] The global barrel has the named export, props type, and reuse comment.
- [ ] Run `git -c core.autocrlf=false -c core.whitespace=cr-at-eol diff --check`.
- [ ] If TypeScript validation is requested, fix only target-specific errors.
- [ ] Return a concise completion message to the orchestrator; do not create a worker report.
