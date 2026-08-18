# Migrate Page to App Router

> Version: 1.0

## Objective

The job MUST create a maintained App Router landing-page scaffold when the target page does not exist, or align an existing App Router landing page with its confirmed legacy-page requirements and documented data contracts.

The job MUST NOT redesign or create organisms, inspect, add, remove, replace, or modify an existing journey-screen import or its rendered JSX invocation, or overwrite an existing page through the scaffolding script.

## Inputs

The job MUST receive:

- an App Router target page path;
- a confirmed legacy page path;

The job MAY receive:

- a valid landing-page slug for contentful.
- App Router page-migration documentation;
- documented contracts for `getLandingDataV2`, `LandingDataOptions`, and `pageSeoToMetadata`; and
- explicit metadata, leads-modal, structured-data, or route-behavior constraints.

Examples:

```txt
Target: src/app/credit-cards/page.tsx
Legacy: src/pages/credit-cards.tsx
Contentful slug: credit-cards
```

## Scope

The agent MAY inspect the confirmed legacy page, the supplied App Router migration documentation, and the supplied contract documentation.

The agent MAY modify the target App Router page path.

The agent MUST NOT modify organism implementations, unrelated routes, or the confirmed legacy page unless the user explicitly requests it.

## Process

### Scaffold Path

1. The job MUST receive an App Router target page path, a confirmed legacy page path
    1.1. `slug` MUST be derived from the legacy page path, if no slug found, halt execution and ask user for a page slug.
2. The job MUST execute `node /scripts/custom/scaffold-landing-page.mjs <target-page-path> <page-slug>`.
3. When the script succeeds, the job MUST continue with the New-Page Alignment path. It MUST NOT add hero or section organisms to `LandingPage` during that path.
4. When the script fails only because the target page already exists, the job MUST continue with the Existing-Page Alignment path. For every other script failure, the job MUST abort and report the error.

### New-Page Alignment

5. The job MUST inspect the confirmed legacy page and fill only the scaffolded page-level configuration from its requirements: `heroSection` mapper; ordered `sections` request entries; `pageSeoToMetadata` overrides; `LeadsProvider` options; and `PageJsonLd` presets.
6. The job MUST preserve the scaffold's imports, declarations, functions, wrappers, `Navbar`, `PreFooterBanner`, and `Footer`.
7. The job MUST NOT import, add, render, configure, or migrate hero or section organisms in `LandingPage`.

### Existing-Page Alignment: Evidence

8. The job MAY read the App Router page-migration documentation supplied by context. When that documentation is unavailable; it MUST NOT use another route as a reference.
9. The job MUST read the documented contracts for `getLandingDataV2`, `LandingDataOptions`, and `pageSeoToMetadata`. When those contracts are not received through Context Output, the job MUST read `getLandingDataV2` from `@shared/utils/contentful-data/contentful-data.util`, `LandingDataOptions` from `@core/types/contentful-data.types`, and `pageSeoToMetadata` from `@shared/utils/contentful-metadata/contentful-metadata.util`.
10. The job MUST inspect the confirmed legacy page only to derive its ordered hero and section identifiers, mapper needs, metadata overrides, structured-data requirements, and leads-modal behavior.
10.1. The job MUST classify each relevant target-page construct as a section or a non-section component before deciding whether it affects page composition.
10.2. The job MUST treat a journey screen as a non-section component. It MUST preserve its import and rendered invocation and MUST NOT use it to decide that a required standard page element may be omitted.
10.3. The job MUST use only classified sections to derive section request entries (i.e. `sections` on `getLandingDataV2`) and section-rendering decisions (i.e. maintain sections on layout).
10.4. It MUST preserve applicable existing configuration, including provider options, metadata overrides, structured-data presets, and route behavior.
10.5. The job MUST identify the required standard page elements independently of sections: `LeadsProvider`, `Navbar`, `PreFooterBanner`, and `Footer`. These sections MUST be included unless the user explicitly express otherwise.
11. The job MUST preserve every existing import, metadata override, provider setting, organism integration, section, and route behavior that does not conflict with the documented contracts or confirmed legacy requirements.

### Existing-Page Alignment: Imports and Declarations

12. The job MUST make the target page's import block and module declarations conform to the structure shown below. It MUST preserve non-conflicting imports and MUST NOT infer, add, remove, or change organism imports.

```tsx
import { cache } from "react";
import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { getLandingDataV2 } from "@shared/utils/contentful-data/contentful-data.util";
import { pageSeoToMetadata } from "@shared/utils/contentful-metadata/contentful-metadata.util";
import { LeadsProvider } from "@journeys/leads/resources/providers";
import { PageJsonLd } from "@shared/components/molecules";
import { Navbar, PreFooterBanner, Footer } from "@shared/components/organisms";

export const dynamic = "force-static";

const PREVIEW = false;
const PAGE_SLUG = "<page-slug>";
```

### Existing-Page Alignment: Data Function

13. The job MUST make `getProps` conform to the structure shown below: a cached function that calls `getLandingDataV2(PREVIEW, PAGE_SLUG, options)` and invokes `notFound()` for a missing landing entry. It MUST preserve existing hero and section request configuration and MUST NOT add heroSection or section entries.

```tsx
const getProps = cache(async () => {
  const landing = await getLandingDataV2(PREVIEW, PAGE_SLUG, {
    heroSection: { mapper: "liquidSection" },
    sections: [/* equivalent legacy sections in order */],
  } as const);

  if (!landing) notFound();
  return landing;
});
```

### Existing-Page Alignment: Metadata Function

14. The job MUST make `generateMetadata` conform to the structure shown below: it obtains `pageSeo` through `getProps` and returns `pageSeoToMetadata(pageSeo, overrides)` or just `pageSeoToMetadata(pageSeo)`. It MUST preserve existing additional metadata, including Open Graph and keywords, unless it conflicts with confirmed legacy requirements.

```tsx
export async function generateMetadata(): Promise<Metadata> {
  const { pageSeo } = await getProps();
  return pageSeoToMetadata(pageSeo, overrides);
}
```

### Existing-Page Alignment: Default Page Component

15. The job MUST make `LandingPage` conform to the structure below: it obtains `props` from `getProps`; includes `LeadsProvider`, `PageJsonLd`, `Navbar`, `PreFooterBanner`, and `Footer`; preserves applicable existing provider options and metadata configuration; and retains any existing non-section screen import and rendered invocation unchanged.

```tsx
export default async function LandingPage() {
  const props = await getProps();

  return (
    <LeadsProvider
      {...props.leadsFormModalOptions}
      disableAutoOpen={true} // options example
      delayByScroll={true} // options example
    >
      <PageJsonLd 
        presets={["creditCard", "organization"]} // presets example
        structuredData={props.structuredData} 
       />
      <Navbar
        enableOneLink={props.navBarLinkOptions.enableNavBarOneLink}
        oneLinkChannel={props.navBarLinkOptions.navBarOneLinkChannel}
      />
      {/* Equivalent migrated sections in legacy order. */}
      {props.sections.preFooterBannerSection && (
        <PreFooterBanner
            className="io-mt-86 io-mt-xl-160"
            {...PreFooterBanner.propsEngine(props.sections.preFooterSection)}
        />
      )}
      {props.footerSection && (
        <Footer {...Footer.propsEngine(props.footerSection)} />
      )}
    </LeadsProvider>
  );
}
```

### Existing-Page Alignment: Boundaries and Reporting

16. The job MUST NOT use a journey-screen handoff for page composition.
17. The job MUST NOT create or redesign organism.

## Output

The job MUST produce Project Output consisting of the scaffolded or aligned App Router page. Every successful completion MUST produce the skill-defined Context Output.

Output generation and page alignment are executed manually by the agent; initial page scaffolding is executed deterministically by script.

**Code / Directory Structure Output**

```txt
<target-page-path>
```

On failure, the agent MUST report the missing prerequisite, invalid input, target path, or scaffolding failure.

## Prompt examples

```txt
Execute migrate-page-to-app-router job for:

Target: app/(landing-page)/nuestra-app/page.tsx
Legacy: pages/nuestra-app-deprecated.tsx
Contentful slug: nuestra-app
```

```txt
Execute migrate-page-to-app-router for src/app/credit-cards/page.tsx using src/pages/credit-cards.tsx, slug credit-cards, and the supplied App Router migration documentation.
```

```txt
Migrate the existing App Router page src/app/loans/page.tsx from src/pages/loans.tsx with slug loans. Use the provided getLandingDataV2, LandingDataOptions, and pageSeoToMetadata contracts.
```
