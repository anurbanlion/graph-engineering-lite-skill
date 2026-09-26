# Worker 9 — Atom and Molecule Storybook

## Responsibility

Provide Storybook coverage only for atoms and molecules newly created or materially changed by Worker 8. Keep fixture data inside each story file and never change organisms, routes, analytics, legacy pages, indexes, or unrelated stories.

## Authoritative references

- `.loop/orchestration/guidelines-migration/dependency-diagram.md` is the authoritative W9 job definition: prepare story-local fixture data, create atom stories, then create molecule stories, after W8 publishes the relevant artifacts.
- `.loop/rules/RULES.md` defines the shared-component layout and required diff validation command.

## Useful queries
- To locate candidate coverage, use:

```powershell
rg --files src/shared/components | Select-String '\\.(stories|component)\\.tsx$'
```

- To identify W8 changes before authoring a story, use:

```powershell
git diff --name-only
```

## Durable rules

- W9 MUST inspect W8's scoped outcome first; it MUST NOT add speculative coverage when W8 created nothing.
- Fixture data MUST live in the `.stories.tsx` file for an atom or molecule.
- When coverage is warranted, stories SHOULD include `Default`, `Long Rich Full Content`, and `Empty` when those states make sense for the artifact.
- Atoms and molecules MUST use only `@shared/` utilities.
- Analytics hooks, including `useTracking` and `TrackedAction`, MUST be called only inside an organism; W9 MUST NOT introduce them in atom or molecule stories.
- Organisms are published through `src/shared/components/organisms/index.ts`; atom/molecule publication uses their own named-export barrels.

## Reusable Storybook pattern

```tsx
export const Default: Story = {
  args: {
    // Fixture data belongs here.
  },
};
```

## Useful commands

```powershell
git -c core.autocrlf=false -c core.whitespace=cr-at-eol diff --check
rg --files src/shared/components | Select-String 'stories.tsx$'
```

## Pitfalls

- Do not infer a story requirement from an organism story; W9 owns only W8-produced atoms and molecules.
- Do not create fixtures files for W9; fixture data belongs in the story file.
- Do not run npm scripts unless explicitly requested.
- Do not use plain `git diff --check`; it can report false whitespace issues after line-ending conversion.

## Handoff guidance

- Confirm W8 has completed for the target organism.
- Identify only atoms/molecules created or changed by W8.
- Add story-local fixtures and relevant variants when an artifact exists.
- Keep all tracking out of atoms, molecules, and their stories.
- Run the required diff validation.
- Return only a concise completion message.
