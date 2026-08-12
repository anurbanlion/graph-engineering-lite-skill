# Plan Page Tagging

## Objective

The job MUST receive a new implementation and MAY receive a confirmed reference implementation.

The job MUST analyze both implementations if possible and MUST produce a section-based migration checklist.

## Inputs

The job MUST receive:

- An app router page implementation path.
- A domain.

The job MAY receive:

- A reference implementation path.

## Process

1. The agent MUST verify that the new implementation is available or create it otherwise.
2. If a reference implementation was supplied, the agent MUST use it as the comparison source.
3. If no reference implementation was supplied, the agent MAY search only within `pages/` for a plausible equivalent of the new page.
4. When a plausible equivalent is found, the agent MUST present its file link and MUST wait for explicit user confirmation before reading or using it as the reference.
5. When no single plausible equivalent is found, the agent MUST request the correct reference implementation from the user.

6. After both implementations are available, the agent MUST inventory their rendered sections in order and MUST create one checklist row per target-page section and tag pair. The `Section` value MAY repeat when a section has multiple tags.
7. Each checklist item MUST identify the section, old tag, new tag identifier, Tracking API, and status.
8. The agent MUST produce a section-based migration plan and MUST NOT perform implementation work.

## Output

The job MUST produce a Managed Output containing a migration checklist organized by target-page section.

The Managed Output MUST use the following table columns, in this order:

| Section | Old Tag | New Tag | Tracking API | Status |
| --- | --- | --- | --- | --- |

The `Old Tag` value MUST identify the legacy component, callback, and tag in the form `<Component>.<callback>.<tag>`.

The `New Tag` value MUST identify the new analytics callback and tag identifier in the form `<callback>: <identifier>` when one exists; otherwise, it MUST propose one.

The `Tracking API` value MUST be `useTracking` or `TrackedAction`. The job MUST select one of these APIs even when the new implementation currently uses a declarative `analytics` prop.

The `Status` value MUST be one of `planned`, `implemented` or  `error`.

The mandatory Context Output MUST link the generated Managed Output under the `plan-page-tagging` job identifier.

Example:

```md
- **plan-page-tagging**:
  - [Page Tagging Migration Plan](path/to/link.md)
```

```md
# Page Tagging Migration Plan

Reference implementation: @pages/index-deprecated.tsx

| Section | Old Tag | New Tag | Tracking API | Status |
| --- | --- | --- | --- | --- |
| Hero carousel | `HeroCarousel.onFormSubmitError.offerViewFormErrorTag` | `formSubmitError: home.offerViewFormError` | `useTracking` | implemented |
| Showcase banner | `ShowcaseBanner.onCtaClick.joinThousandsCustomersTag` | `joinThousandsCustomersClick: home.joinThousandsCustomersClicked` | `TrackedAction` | implemented |
| Feature carousel | `FeatureCarousel.onCtaClick.startYourApplicationNowTag` | `ctaClick: home.startYourApplicationNow` | `TrackedAction` | implemented |
| Video carousel | `VideoCarousel.onStartVideoClick.startVideoTag` | `startVideoClick: home.startVideo` | `useTracking` | implemented |
| Conversion banner | `ConversionBanner.onCtaClick.knowBenefitsTag` | `ctaClick: home.knowBenefitsTrack` | `TrackedAction` | implemented |
```

On failure, the agent MUST report the missing new implementation, reference confirmation, or reference implementation.

## Prompt examples

```txt
Execute the plan-page-tagging job with:

- New implementation: app/page.tsx
- Reference implementation: pages/index-deprecated.tsx
```
