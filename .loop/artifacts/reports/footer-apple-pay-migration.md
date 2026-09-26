# Report - Footer Apple Pay migration

## Completed Tasks

- `migrate-analytics-to-shared-organism`: completed. Footer now owns its tracking through the registered `common.footerActionClicked` target; no public `analytics` or `enableTracking` switch is exposed.
- Legacy audit: the deprecated Apple Pay page renders the legacy Footer without an Apple Pay-specific callback. Footer interactions were legacy `click_element` events with `section: footer`, a subsection, and the selected label. No perceptible Footer action is untracked in the migrated implementation: section links, linked badges, and social links are handled internally.
- `migrate-organism-into-journey`: completed. Apple Pay already rendered the shared `Footer` from `@shared/components/organisms` with `Footer.propsEngine(props.footerSection)`. The modernized organism is therefore wired without an additional page diff or analytics prop; the checklist now records the migration, Storybook, and taggeos.
- Parity correction: completed. The reusable schema and every Footer caller now emit the legacy-compatible `event_data.subSection` field rather than `sub_section`; self-contained tracking and the public API remain unchanged.

## Artifacts

- [common.schemas.ts](../../analytics/schemas/common.schemas.ts): registered `common.footerActionClicked` in the common registry, with the reusable footer context.
- [footer.component.tsx](../../src/shared/components/organisms/footer/footer.component.tsx): removed legacy tracker/`enableTracking` dependency; social links track internally.
- [footer.props.ts](../../src/shared/components/organisms/footer/footer.props.ts): removed the caller-controlled `enableTracking` prop.
- [footer-section.component.tsx](../../src/shared/components/molecules/footer-section/footer-section.component.tsx): migrated linked section items and badges from the legacy footer tracker.
- [footer-link.component.tsx](../../src/shared/components/organisms/footer/resources/components/footer-link/footer-link.component.tsx) and [footer-bottom-bar.component.tsx](../../src/shared/components/organisms/footer/resources/components/footer-bottom-bar/footer-bottom-bar.component.tsx): migrated retained Footer resources to the common target and removed `enableTracking`.
- [routes-components-checklist.md](../../.graph-engineering/artifacts/routes-components-checklist.md): records Apple Pay `Footer` as migrated, storybook-covered, and analytics-tagged.
- [Apple Pay page](../../app/(landing-page)/apple-pay/page.tsx): verified existing shared Footer rendering and Contentful props-engine configuration; intentionally unchanged for this job.
- [Apple Pay parity report](./apple-pay-pre-footer-footer-parity-report.md): identified the `subSection` field-name correction that this update resolves.

## Commands and Tool Calls

| Type | Command or tool | Purpose | Outcome |
| --- | --- | --- | --- |
| Console | `Get-Content` for Loop rules/jobs, checklist, docs, Footer, Navbar, schemas, Apple Pay pages | Establish constraints, legacy behavior, and Navbar reference | Completed; deprecated page read only. |
| Search | `rg` for Footer renderers, `trackFooterClick`, and `enableTracking` | Locate all direct callers and Footer tracking paths | Completed; all Footer-specific legacy tracking paths migrated. |
| Internal tool | Collaboration message to orchestrator | Reserve `analytics/schemas/common.schemas.ts` before its shared-registry edit | Acknowledged; no overlap. |
| Console | `git diff --check` | Check patch whitespace | Completed with no diff errors. |
| Search | `rg '<Footer\\b|Footer\\.propsEngine'` | Verify direct production Footer renderers and Apple Pay wiring | Apple Pay and other production callers use `Footer.propsEngine`; no caller configuration is needed for self-contained tracking. |
| Search | `rg 'sub_section|subSection|common.footerActionClicked'` scoped to Footer and the common schema | Verify the corrected external field name at schema and every Footer call site | Only legacy-compatible `subSection` remains. |

## Verification

- `rg` confirms `common.footerActionClicked` is registered and used by Footer social links, section links, badges, and retained Footer resources.
- `rg` confirms no `trackFooterClick` or `enableTracking` remains in active Footer code. The legacy footer tracker remains only for the separately-owned PreFooter legacy path.
- Apple Pay retains the legacy-equivalent ordering: PreFooterBanner followed by Footer; the legacy reference page was not changed.
- Apple Pay's Footer has no analytics prop by design: it mirrors Navbar's self-contained registered tracking model.
- The common schema and every Footer tracking context now preserve legacy `event_data.subSection` naming.
- No npm script was run, per repository instruction.
- Direct production Footer renderers were identified. Because tracking is self-contained, they require no prop configuration.

## Unresolved Issues

- None. Await reviewer feedback and the subsequent joint parity verification.
