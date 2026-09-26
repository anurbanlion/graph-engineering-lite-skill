# Review - Apple Pay Footer and PreFooterBanner migration

## Verdict

Approved

## Verified Outcomes

- **Footer — approved in reviewer round 1.** The shared registry defines `common.footerActionClicked`; current Footer section links, badges, social links, and retained Footer resources call it internally through `useTracking`. `FooterProps` no longer exposes `enableTracking`, which matches the explicit Navbar-like, self-contained tracking requirement.
- **Footer journey wiring — approved.** Apple Pay already renders `Footer` through `Footer.propsEngine(props.footerSection)` after `PreFooterBanner`; its self-contained tracking needs no renderer configuration. The Apple Pay checklist marks Footer as migrated, Storybook-covered, and tagged.
- **PreFooterBanner contract and wiring — structurally verified.** The organism exposes optional `analytics.ctaClicked`, owns the CTA context, and uses `TrackedAction`; `PreFooterCta` has no direct legacy tracker call. `common.ctaClicked` is a valid registered common target.
- **PreFooterBanner renderer coverage — verified.** One targeted renderer search found ten direct production renderers, and a single focused context search confirmed `analytics={{ ctaClicked: "common.ctaClicked" }}` in each. Storybook files were excluded.
- **Apple Pay journey structure — verified.** Apple Pay uses the shared PreFooterBanner mapper, configures its target, preserves the reported animation/title alignment/spacing, then renders the shared Footer. The checklist now records PreFooterBanner as migrated and tagged.
- **PreFooterBanner correction — approved.** The CTA now emits the legacy-equivalent context through the registered common target: `section: "pre-footer"` and lower-cased button text for `option`. The scoped whitespace check passed.
- **Joint parity and Footer correction — approved in reviewer round 2.** The joint parity report identified a legacy event-data key mismatch, assigned it to the Footer worker, and records its correction. The common schema and every scoped Footer call site now consistently use legacy-compatible `subSection`; the parity rerun passed.

## Findings

| Severity | Finding | Evidence | Required Correction |
| --- | --- | --- | --- |
| None | The prior P1 PreFooterBanner context-mapping finding is resolved. | [Updated worker report](./pre-footer-banner-migration-report.md) and [implementation](../../src/shared/components/organisms/pre-footer-banner/pre-footer-banner.component.tsx) show `section: "pre-footer"` with `button?.text?.toLowerCase() ?? ""`. | None. |
| None | The parity-reported Footer `sub_section` versus `subSection` payload-key difference is resolved by the Footer worker. | [Parity report](./apple-pay-pre-footer-footer-parity-report.md) records the finding, worker ownership, rerun, and pass; the scoped schema/call-site evidence confirms `subSection`. | None. |

## Required Corrections

- None. Both component workers are ready for the joint final parity verification.

## Evidence Strategy and Call Minimization

- I read the two worker reports, the required Loop/analytics rules, the analytics documentation, the Apple Pay checklist, and only artifacts directly linked by those reports.
- I used one scoped diff for the changed component/schema/journey files; two narrow searches checked legacy-call removal/tracker use and direct renderer discovery; one focused renderer-context search established all ten PreFooterBanner configurations. I did not scan unrelated project areas, run package scripts, or re-read deprecated pages; the deprecated route remained reference-only.
- Further evidence was necessary only for the report's direct-renderer claim and was obtained with the focused context search above. No broader reads are needed until the PreFooterBanner correction arrives or the later parity-review round is assigned.
- **Correction re-review:** I read the updated worker report, inspected only the changed `TrackedAction` context lines, and ran one scoped `git diff --check`. This avoided repeating renderer, schema, journey, or deprecated-reference reads because the correction did not affect them.
- **Reviewer round 2:** I used the final joint parity report and final worker reports as primary evidence, then ran one scoped schema/call-site check and one scoped whitespace check for the only parity correction. I did not re-read legacy pages, journey renderers, or PreFooterBanner artifacts because the parity report documented them as unaffected; no runtime, browser, npm, or broad-repository calls were necessary.
