# Report - PreFooterBanner analytics and Apple Pay migration

## Completed Tasks

- `migrate-analytics-to-shared-organism`: Completed. `PreFooterBanner` now exposes the optional serializable `analytics.ctaClicked` target, maps its own CTA context, and tracks through `TrackedAction`.
- Legacy CTA tracking removal: Completed. `PreFooterCta` no longer calls `trackFooterClick`; it remains a presentational clickable control that receives the wrapper-provided click handler.
- Direct production renderer configuration: Completed. Every discovered direct production `PreFooterBanner` renderer opts into `common.ctaClicked`.
- `migrate-organism-into-journey`: Completed. Apple Pay now uses the shared `PreFooterBanner` with the same reference content mapper, mobile oscillating animation, bottom title alignment, and responsive spacing.
- Reviewer round-1 correction: Completed. Restored the legacy-equivalent CTA context semantics while retaining registry-backed `common.ctaClicked` tracking.

## Analytics Audit

| Legacy interaction | Legacy event/context | New target/context | Outcome |
| --- | --- | --- | --- |
| Pre-footer CTA click | `trackFooterClick({ section: "pre-footer", option: button.text?.toLowerCase() })` | `common.ctaClicked` with `{ section: "pre-footer", option: button.text?.toLowerCase() }` | Migrated to registry-backed shared tracking with legacy-equivalent segmentation. |

- Schema and registry: existing [`common.ctaClicked`](../../analytics/schemas/common.schemas.ts) in the common registry; no schema or registry change was necessary.
- Organism API: [`PreFooterBannerProps`](../../src/shared/components/organisms/pre-footer-banner/pre-footer-banner.props.ts) adds `analytics?.ctaClicked?: TrackingTarget<PreFooterBannerCtaClickedContext>`.
- Wiring: [`PreFooterBanner`](../../src/shared/components/organisms/pre-footer-banner/pre-footer-banner.component.tsx) owns the context mapping and wraps its CTA in `TrackedAction`.

## Artifacts

- [`PreFooterBanner` props](../../src/shared/components/organisms/pre-footer-banner/pre-footer-banner.props.ts): Added the typed optional analytics contract.
- [`PreFooterBanner` component](../../src/shared/components/organisms/pre-footer-banner/pre-footer-banner.component.tsx): Added organism-owned `TrackedAction` wiring.
- [`PreFooterContent`](../../src/shared/components/molecules/pre-footer-content/pre-footer-content.component.tsx): Accepts the organism-owned CTA node.
- [`PreFooterCta`](../../src/shared/components/molecules/pre-footer-cta/pre-footer-cta.component.tsx): Removed direct legacy tracking and forwards its supplied click handler.
- [`Apple Pay`](../../app/(landing-page)/apple-pay/page.tsx): Configures `analytics={{ ctaClicked: "common.ctaClicked" }}`.
- [`Apple Pay route checklist`](../../.graph-engineering/artifacts/routes-components-checklist.md): Marks `PreFooterBanner` as migrated with analytics support; the organism has no Storybook story file, so that cell remains blank.
- Direct production renderers: [`home`](../../app/(landing-page)/page.tsx), [`Nuestra App`](../../app/(landing-page)/nuestra-app/page.tsx), [`Referidos`](../../app/(landing-page)/referidos/page.tsx), [`Tarjeta de Crédito`](../../app/(landing-page)/tarjeta-de-credito/page.tsx), [`Beneficios`](../../src/journeys/landing-page/beneficios/screens/beneficios/beneficios.screen.tsx), [`Blog`](../../src/journeys/landing-page/blog/screens/blog/blog.screen.tsx), [`Blog post`](../../src/journeys/landing-page/blog/screens/blog-post/blog-post.screen.tsx), [`Podcast`](../../src/journeys/landing-page/podcast/screens/podcast/podcast.screen.tsx), and [`Podcast post`](../../src/journeys/landing-page/podcast/screens/podcast-post/podcast-post.screen.tsx): Configured the shared CTA target.

## Commands and Tool Calls

| Type | Command or tool | Purpose | Outcome |
| --- | --- | --- | --- |
| Console | `Get-Content -Raw .loop/rules/...` | Read the required global and analytics rules and authorized jobs. | Completed. |
| Console | `Get-Content -Raw analytics/docs/...` | Read all analytics documentation. | Completed. |
| Search | `rg -n -i "PreFooterBanner|PreFooter|trackFooter..." ...` | Locate the legacy behavior, organism, App Router target, and direct renderers. | Found one CTA interaction and ten production renderers. |
| Search | `rg -n ... common.ctaClicked ...` | Find a compatible registered shared schema. | Reused `common.ctaClicked`. |
| Internal tool | `apply_patch` | Implement the analytics contract, tracking wiring, legacy-call removal, and renderer configuration. | Completed; no legacy page modified. |
| Console | `rg ...; git diff --check; git diff ...` | Verify renderer coverage, legacy-call removal, whitespace, and scoped diff. | Renderer coverage is complete; no whitespace errors; no CTA legacy tracker remains. |
| Console | `rg -n -C 5 '<PreFooterBanner' pages/apple-pay-deprecated.tsx app/(landing-page)/apple-pay/page.tsx` | Compare Apple Pay reference placement and configuration with the migrated journey. | Matched section source, `animation.mobile`, `titleAlign`, and spacing after breakpoint conversion (`lg` to `xl`). |
| Console | `rg ... section: "pre-footer" ...; git diff --check` | Verify reviewer correction, absence of legacy CTA tracking, and whitespace. | Context now uses the expected section and lower-cased option; no legacy call or whitespace error. |

## Verification

- `PreFooterBanner` has one perceptible interaction: its CTA.
- The CTA has an optional, serializable, action-specific analytics target and uses the existing common registry schema.
- The legacy Pages Router Apple Pay page was read only; it was not modified.
- All discovered direct production renderers configure `common.ctaClicked`; Storybook renderers were excluded.
- Apple Pay maps the same Contentful pre-footer section through `PreFooterBanner.propsEngine`, keeps `animation={{ mobile: "oscillating" }}`, keeps `titleAlign="bottom"`, and maps legacy `io-mt-lg-131` to the App Router `io-mt-xl-131` utility.
- The reference page's `io-mt-59` margin is preserved.
- Reviewer round-1 correction preserves legacy CTA dimensions: `section` is the stable `"pre-footer"` value and `option` is `button.text.toLowerCase()` with an empty-string fallback for the unreachable no-button case.
- `git diff --check` completed without whitespace errors.
- No npm scripts were run, per repository instruction.

## Unresolved Issues

- None.
