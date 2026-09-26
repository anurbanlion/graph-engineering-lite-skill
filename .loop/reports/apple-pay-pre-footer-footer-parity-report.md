# Report - Apple Pay PreFooterBanner and Footer parity

## Completed Tasks

- `verify-component-parity`: rerun jointly for the migrated `PreFooterBanner` and `Footer` in Apple Pay after the Footer correction. Result: **pass**.
- `report`: updated this living parity report in place with the correction evidence and final verdict.

## Artifacts

- [Apple Pay parity report](./apple-pay-pre-footer-footer-parity-report.md): living evidence and verdict for both organisms.
- [Legacy Apple Pay page](../../pages/apple-pay-deprecated.tsx): read-only reference for placement, props, and legacy components; not modified.
- [App Router Apple Pay page](../../app/(landing-page)/apple-pay/page.tsx): target journey evidence.
- [PreFooterBanner implementation](../../src/shared/components/organisms/pre-footer-banner/pre-footer-banner.component.tsx): CTA tracking and interaction evidence.
- [Footer common schema](../../analytics/schemas/common.schemas.ts): registered target payload evidence.
- [Legacy Footer tracker processor](../../analytics/processors/footer.processor.ts): legacy event-data field evidence.

## Verification

| Requirement | Evidence | Result |
| --- | --- | --- |
| PreFooterBanner source, location, and configuration are preserved | Legacy Apple Pay lines 96-102 and App Router lines 94-101 both map the `pre-footer-banner` section, set `animation.mobile` to `oscillating`, set `titleAlign` to `bottom`, and place it immediately before Footer. The target preserves `io-mt-59`; its desktop breakpoint utility changes from `lg-131` to `xl-131`, consistent with the migrated page utilities. | Pass |
| PreFooterBanner CTA behavior and analytics payload are equivalent | Legacy `components/Common/PreFooterBanner.tsx` lines 100-110 invokes the footer tracker with `section: "pre-footer"` and lower-cased button text. The shared organism wraps the same CTA in `TrackedAction` with that context; Apple Pay configures `common.ctaClicked`. The common schema emits `io.event` / `click_element`, `element_type: "button"`, the same section, and the same option. | Pass |
| Footer is self-contained and has no public tracking control | `FooterProps` has no `analytics` or `enableTracking` prop; Apple Pay renders `Footer.propsEngine(props.footerSection)` without one. Current shared footer controls use the internal registered `common.footerActionClicked` target. | Pass |
| Footer clickable controls preserve event name and core context | Legacy tracker tag sends `io.event` / `click_element` with `element_type: "button"`; shared schema has those same values. Shared links, badges, and social controls supply `section: "footer"` and the legacy-equivalent control label. | Pass |
| Footer event-data field names are equivalent | The legacy processor writes the footer grouping key as `subSection`; the corrected common schema and every checked Footer call site now use `subSection`. | Pass |
| Footer visual parity | Footer has Storybook coverage according to the Apple Pay checklist, so this job verifies functionality, mapper/journey wiring, and tracking rather than pixel-level styling, per the parity job scope. | Pass / visual comparison out of scope |

## Approved Differences

- The App Router's responsive utility uses `xl` where the legacy Pages Router uses `lg` for the PreFooterBanner desktop margin. The earlier worker report documents this migration-specific breakpoint conversion while retaining the values and intended spacing.
- Footer's analytics ownership changed from the legacy caller-controlled testing flag to self-contained common-registry tracking. This is an explicit task requirement.

## Unresolved Issues

- None. The Footer worker restored legacy-compatible `subSection` in the shared schema and every checked Footer call site; the joint verdict is **pass**.

## Commands and Tool Calls

| Type | Command or tool | Purpose | Outcome |
| --- | --- | --- | --- |
| Console | `Get-Content` for required Loop rules/jobs, analytics rules/docs, supplied reports, and route checklist | Establish job contract and consume prior evidence before source reads | Completed |
| Search | Scoped `rg` on legacy/target Apple Pay pages, common schema, and direct PreFooter/Footer implementations | Compare only the two organisms' journey configuration, interactions, and payloads | Found the Footer `subSection` / `sub_section` discrepancy |
| Console | `Get-Content` for legacy footer tracker and processor | Validate the actual legacy event shape, not only worker-report claims | Confirmed legacy processor emits `subSection` |
| Console | Scoped `git diff --check` and `git diff` | Check worker changes and whitespace without running project scripts | No whitespace errors; diff confirms the field rename |
| Internal tool | `apply_patch` | Create this living parity report | Completed |
| Console | Focused `Get-Content`, scoped `rg`, and scoped `git diff --check` after Footer correction | Recheck only the prior unresolved payload-field gap | Confirmed `subSection` in the legacy processor, shared schema, and every checked Footer call site; no whitespace errors |

## Read and Call Minimization

- Read the supplied worker and reviewer reports first, then inspected only their cited Apple Pay, organism, schema, legacy tracker/processor, and `TrackedAction` evidence.
- Used narrow path-scoped searches instead of repository-wide renderer or tracker scans. No production files were changed, no deprecated file was modified, and no npm script or browser/runtime call was run.
- The additional legacy tracker/processor read was necessary only to test the parity job's exact sent-event-data requirement; it exposed the unresolved field-name difference.
- For the rerun, read only the Footer correction report and rechecked the previously failing schema/call sites plus the already-cited legacy processor. PreFooterBanner evidence was not reread because its prior result was unaffected.
