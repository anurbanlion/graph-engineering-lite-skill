# Worker 2: Fixtures and Storybook

## Responsibility

Worker 2 owns contract-valid local fixtures and Storybook coverage for migrated organisms. The normal scope is limited to `<organism>.fixtures.ts` and `<organism>.stories.tsx`. Expand that scope only when explicitly assigned to support a fixture-driven Storybook state.

## Authoritative references

- `.loop/artifacts/RULES.md` for organism layout, import rules, and validation.
- The target organism's `<organism>.props.ts` and `propsEngine` for the normalized public data shape.
- The target organism's `<organism>.component.tsx` for rendered fields, required interaction props, and valid empty states.
- The target organism's `index.ts` for the local barrel export used by stories.
- Directly comparable fixture/story pairs only when the target contract does not make the intended representation clear.

## Scope boundaries

- Do not change legacy pages or components.
- Do not change route integration, analytics, global barrel publication, props normalization, styles, or organism implementation unless the assignment explicitly requires it.
- Do not create reviewer, reformer, review-queue, or worker-report artifacts.
- Reuse this worker identity for fixtures and Storybook work; it is not tied to a Gantt time unit.

## Durable rules

- Fixture exports use lower camel case and end in `Fixture`.
- Fixtures must satisfy the current public props contract. Do not retain removed field aliases.
- Use `mockRichText` from `@shared/utils/frontend` for rich-content variants.
- Stories use `Meta`/`StoryObj`, import the organism from local `./index`, and import data from local `./<organism>.fixtures`.
- Use `Default`, `LongRichFullContent`, and `Empty` where the contract supports those states. Default should have a journey-specific display name.
- Home stories use exactly `Shared/Organisms/Home/<Component>` for HeroCarousel, ShowcaseBanner, VideoCarousel, ConversionBanner, ReviewsCarousel, and BlogCarousel.
- Model only interaction APIs supported by the component. For example, VideoCarousel supports `startVideo`; do not invent `stopVideo`.
- Preserve supplied reference text and assets. Do not add visible labels or titles absent from the reference.
- Apply `?w=700&fm=avif&q=80` to Contentful fixture image URLs when image optimization is required; preserve URLs exactly when an assignment provides exact assets.
- Required props remain required in Empty stories. For example, BlogCarousel uses `{ blogs: [] }`; optional-only contracts may use `{}`.
- Rich content takes precedence over plain fallback text. Put all required visible rich paragraphs in `richDescription` rather than splitting them across fallback and rich fields.
- For Storybook-only visibility needs, use a neutral optional configuration and enable it only in the fixture. Do not globally enable production behavior.

## Reusable pattern

```ts
import type { Meta, StoryObj } from "@storybook/react";
import { Organism } from "./index";
import {
  emptyFixture,
  journeyFixture,
  longRichFullContentFixture,
} from "./organism.fixtures";

const meta = {
  title: "Shared/Organisms/Journey/Organism",
  component: Organism,
  parameters: { layout: "fullscreen" },
} satisfies Meta<typeof Organism>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  name: "Default (Journey)",
  args: journeyFixture,
};
```

## Useful PowerShell commands

```powershell
rg --files 'src/shared/components/organisms' | rg '<organism>'
rg -n 'type <Type>|<OrganismName>' 'src/shared/components' -g '*.ts' -g '*.tsx'
Get-Content -LiteralPath 'src/shared/components/organisms/<organism>/<organism>.props.ts'
Get-Content -LiteralPath 'src/shared/components/organisms/<organism>/<organism>.component.tsx'
Get-Content -LiteralPath 'src/shared/components/organisms/<organism>/index.ts'
git -c core.autocrlf=false -c core.whitespace=cr-at-eol diff --check
```

Do not run npm scripts unless explicitly requested.

## Pitfalls

- Plain `git diff --check` can produce CRLF warnings; use the configured command above.
- `git diff` does not show untracked files. Inspect new files with `Get-Content` or `git status --short` when needed.
- Some components return `null` for empty arrays. An Empty story is still valid when required props are supplied.
- Do not invent callbacks or field shapes; inspect the component and contract first.
- Preserve edits made by the user or other workers; re-read target files before patching.

## Handoff checklist

- [ ] Read the target contract, component, and local barrel.
- [ ] Use contract-valid fixture data and lower-camel `*Fixture` exports.
- [ ] Add the required named variants and correct Storybook category.
- [ ] Use local barrel and fixture imports in the story.
- [ ] Preserve explicit reference copy, assets, and interaction boundaries.
- [ ] Stay within W2 ownership unless the assignment explicitly expands it.
- [ ] Validate with:

```powershell
git -c core.autocrlf=false -c core.whitespace=cr-at-eol diff --check
```

- [ ] Return a concise completion message only.
