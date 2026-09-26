# Migrate Organism into Journey

## Description

Given an App Router journey and its pages Router equivalent, add or replace a component with a component organism.

## Preconditions

- The target journey MUST have a Pages Router reference entry page at `pages/<journey>.tsx` or `pages/<journey>-deprecated.tsx`.
- The target journey MUST have an App Router entry page at `app/<journey>/page.tsx`.

- The organism MUST be exported by `src/shared/components/organisms/index.ts`.
- The organism MUST exist under `src/shared/components/organisms/<organism>/`.

- The Worker MUST determine analytics readiness using [Analytics Rules: Organism analytics readiness](../../rules/analytics/RULES.md#organism-analytics-readiness). An organism with perceptible interactions MUST have:
  - the required analytics API;
  - a related registered schema and applicable schema ID; and
  - `useTracking` or `TrackedAction` wiring inside the component.
- Alternatively, an organism with no perceptible interaction is ready with analytics marked `none`.

If the Pages Router reference, App Router entry page, or ready public organism is missing, the Worker MUST stop and communicate to the user or orchestrator. The Worker MUST reuse verified prerequisite evidence already supplied in its context and inspect only prerequisites that remain unknown.

## Inputs

- The reference Pages Router entry page;
- The target App Router entry page;
- The legacy component name; and
- The equivalent shared organism name.

Example:

```md
- Pages Router: `pages/apple-pay-deprecated.tsx`
- App Router: `app/(landing-page)/apple-pay/page.tsx`
- Legacy component: `FeaturesSteps`
- Shared organism: `FeaturesSteps`
```

## Scope

The Worker MUST wire the ready shared organism into the existing journey. The Worker MUST NOT create a journey, implement analytics, schemas that are still missing or modify legacy pages and components.

## Process

1. Import the shared organism into the target App Router page and render it with its normal props. Read the Pages Router reference only to map content, configuration, and behavior. Use `propsEngine` provided by the organism.

   ```powershell
   # Compare the Pages Router reference with the App Router journey before wiring the organism to check analytics, margins and positioning of the organism.
   Get-Content -Raw 'pages/<journey>.tsx'
   Get-Content -Raw 'app/<journey>/page.tsx'
   ```

   ```tsx
   import { SharedOrganism } from "@shared/components/organisms";

   <SharedOrganism
     className="io-mt-60 io-mt-xl-120"
     {...SharedOrganism.propsEngine(props.sections.sharedOrganismSection)}
   />
   ```

2. Add the ready analytics configuration to the target render when the organism has perceptible interactions. The Worker MUST use only the organism's supported analytics slots and registered target IDs; an organism  with no perceptible interaction needs no analytics prop.

   ```tsx
   <SharedOrganism
     {...SharedOrganism.propsEngine(props.sections.sharedOrganismSection)}
     analytics={{
       actionClicked: "common.sharedOrganismActionClicked",
     }}
   />
   ```

3. Find every production App Router reference to the organism and add any missing supported props, analytics configuration, or `io-mt-* io-mt-xl-*` margin utility. The Worker MUST exclude Pages Router references and Storybook.

   ```powershell
   rg -l '<SharedOrganism' app src --glob '!pages/**' --glob '!**/*.stories.*'
   ```

   ```tsx
   <SharedOrganism
     className="io-mt-60 io-mt-xl-120"
     {...SharedOrganism.propsEngine(props.sections.sharedOrganismSection)}
     analytics={{ actionClicked: "common.sharedOrganismActionClicked" }}
   />
   ```

After completing these steps, the Worker MUST run the `report` Job and maintain one living report for this logical task, updating it in place for corrections.

## Output

The Worker report MUST include:

- the old-to-new component map;
- content and configuration mapping;
- the selected organism public API and import path;
- approved differences; and
- the scoped migration diff and verification results.

The output hands the report to the user or the orchestrator.
