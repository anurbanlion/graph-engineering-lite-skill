# Migrate Journey to App Router

## Description

Migrate a complete landing-page journey from Pages Router to App Router by following verified, already-migrated journey examples while preserving the legacy journey's content, backend mapping, and supported shared-organism configuration.

## Preconditions

- The target must have a Pages Router entry page at `pages/<journey>.tsx`.
- The worker must be able to rename that entry page to `pages/<journey>-deprecated.tsx` without overwriting an existing file.
- The target must have, or be approved to receive, `app/(landing-page)/<journey>/page.tsx`.
- The worker must read the target's legacy page and at least two existing App Router journey examples before changing code. Prefer examples with the same shared organisms and layout.

If a precondition is absent, the worker MUST stop and report the missing prerequisite without changing unrelated files.

## Inputs

- Target journey slug;
- Legacy Pages Router page path;
- App Router page path;
- The relevant backend journey data source; and
- Two or three implemented App Router examples, such as:
  - `pages/apple-pay-deprecated.tsx` and `app/(landing-page)/apple-pay/page.tsx`;
  - `pages/nuestra-app-deprecated.tsx` and `app/(landing-page)/nuestra-app/page.tsx`; and
  - `pages/tarjeta-de-credito-deprecated.tsx` and `app/(landing-page)/tarjeta-de-credito/page.tsx`.

## Scope

The worker MUST create or complete the target App Router page, migrate only available shared organisms, preserve target-specific values from the legacy page, and rename the migrated Pages Router entry page to `*-deprecated.tsx`.

The worker MUST NOT change shared components, analytics schemas, or unrelated pages unless explicitly assigned separately.

## Process

1. Read `.graph-engineering/artifacts/routes-components-checklist.md`, `analytics/docs/`, and `openspec/specs/components-conventions/design.md` as reference documentation. The worker MUST NOT invoke an OpenSpec skill or workflow.
2. Compare the legacy page with two or three implemented App Router examples. Identify the target's shared-organism equivalents, content values, class names, analytics configuration, data props, and intentional differences.
3. Implement the page with named imports that comply with the project import conventions. Map journey data through every organism's `propsEngine` rather than duplicating backend mapping in the page.
4. Use this default page shell; include only the optional sections that exist in `props` and place journey-specific migrated organisms between `Navbar` and `PreFooterBanner`:

```tsx
<LeadsProvider {...props.leadsFormModalOptions}>
  <PageJsonLd structuredData={props.structuredData} />
  <Navbar
    enableOneLink={props.navBarLinkOptions.enableNavBarOneLink}
    oneLinkChannel={props.navBarLinkOptions.navBarOneLinkChannel ?? undefined}
  />

  {/* Journey-specific migrated organisms. */}

  {props.sections.preFooterBannerSection && (
    <PreFooterBanner
      className="io-mt-?? io-mt-xl-???"
      {...PreFooterBanner.propsEngine(props.sections.preFooterBannerSection)}
      analytics={{ ctaClicked: "common.ctaClicked" }}
      animation={{ mobile: "oscillating" }}
      titleAlign="bottom"
    />
  )}
  {props.footerSection && (
    <Footer {...Footer.propsEngine(props.footerSection)} />
  )}
</LeadsProvider>
```

5. Replace `??` with the spacing values established by the target's comparable examples and legacy layout; do not leave placeholders in code.
6. Configure only registered, supported analytics targets. For each organism with perceptible interactions, consult `analytics/docs/` and preserve compatible tracker configuration from the examples or legacy page.
7. Rename `pages/<journey>.tsx` to `pages/<journey>-deprecated.tsx` after the new page is in place. The legacy page MUST remain available under the deprecated name.
8. Check the completed page against the legacy page and the route-components checklist. Report the old-to-new component map, intentional differences, renamed file, and validation performed.

## Output

The worker MUST provide:

- the legacy-to-App-Router component map;
- the paths of the App Router page and renamed deprecated page;
- the examples used as migration references;
- the configured analytics targets and any intentionally omitted sections; and
- concise verification results.
