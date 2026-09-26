# Worker 7 — Journey Integration

## Durable responsibility

Worker 7 integrates published shared organisms into App Router journey route
shells. The worker preserves the legacy section sequence, maps Contentful
sections through each organism's `propsEngine`, and passes the analytics
targets selected by the analytics owner.

Tracking implementation belongs inside organisms. Route files MUST NOT call
`useTracking` or `track`; they only provide the organism's `analytics` target
configuration.

## Authoritative references

- `.loop/artifacts/RULES.md` — organism structure, import boundaries, and the
  required line-ending-safe validation command.
- `.loop/orchestration/guidelines-migration/dependency-diagram.md` — worker
  ownership and prerequisites.
- `.loop/orchestration/guidelines-migration/gantt-diagram*.md` — authorized
  time units and scheduling.
- `analytics/docs/GUIDE.md` and `analytics/docs/USAGE.md` — tracker selection
  and route configuration patterns.
- `analytics/schemas/index.ts` — registered tracker IDs.
- `app/(landing-page)/<journey>/page.tsx` — route shell and section mapping.
- `src/shared/components/organisms/<organism>/index.ts` and `*.props.ts` —
  public organism API, `propsEngine`, and analytics property names.
- `pages/<journey>-deprecated.tsx` — reference-only legacy source; it MUST NOT
  be modified.

## Durable rules and pointers

- Import organisms from `@shared/components/organisms`.
- Use `Organism.propsEngine(props.sections.<sectionKey>)` instead of mapping
  Contentful data in the route.
- Preserve the legacy rendering order and keep the route's section guards.
- Use only tracker IDs present in the registry and compatible with the
  organism's analytics contract.
- Choose a reusable/common tracker for reusable component semantics. Do not
  bind a reusable organism to a journey-specific tracker when that would lose
  component context.
- `FeatureCarousel` uses `common.featureCarouselCtaClicked` when its slide and
  CTA context is required; its route property is `ctaClick`.
- `FeaturesList` receives no analytics configuration when its contract has no
  interaction to track.
- When a tracker is renamed, update route references and remove obsolete schema
  declarations and registry entries where applicable.
- Route integration does not include contract, fixture, Storybook, flat
  organism, analytics-schema, or publication work owned by other workers.

## Reusable integration pattern

```tsx
{props.sections.organismSection && (
  <Organism
    {...Organism.propsEngine(props.sections.organismSection)}
    analytics={{ ctaClicked: "common.ctaClicked" }}
  />
)}
```

For an organism with component-specific context:

```tsx
<FeatureCarousel
  {...FeatureCarousel.propsEngine(props.sections.featureCarouselSection)}
  analytics={{ ctaClick: "common.featureCarouselCtaClicked" }}
/>
```

## Useful queries and commands

```powershell
rg -n -C 3 'Organism|Section|analytics|propsEngine' 'app/(landing-page)/<journey>/page.tsx'
rg -n '"<domain>\.<tracker>"' 'analytics/schemas'
git -c core.autocrlf=false -c core.whitespace=cr-at-eol diff --check
```

Use `Get-Content -LiteralPath` for focused inspection of a route, organism
index, or props contract. Do not run npm scripts unless explicitly requested.

## Pitfalls

- Do not move `useTracking` or `track` into `page.tsx`.
- Do not edit `pages/*-deprecated.tsx`.
- Do not replace a new organism with an older organism merely because both
  consume the same Contentful section.
- Do not add analytics to an organism whose contract exposes no interaction.
- Do not assume a Contentful slug is the organism name; follow the route's
  section key and the organism's public `propsEngine`.
- Do not use a legacy tracker ID after its registered schema has been renamed.
- Do not change unrelated organisms or route sections while integrating one
  target.

## Handoff guidance

Before handing off, confirm:

- The required Contentful section is requested by the route.
- The organism is imported from `@shared/components/organisms`.
- The organism is rendered with its `propsEngine`.
- Legacy order and conditional rendering are preserved.
- Analytics targets are registered and match the organism contract.
- No tracking API was added to the route.
- The deprecated legacy page is untouched.
- No unrelated diagram was changed.
- The exact validation command passes:
  `git -c core.autocrlf=false -c core.whitespace=cr-at-eol diff --check`.
