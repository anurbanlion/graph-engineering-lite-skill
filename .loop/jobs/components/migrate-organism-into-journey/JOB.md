# Migrate Organism into Journey

## Description

Replace old component rendering in an existing entry journey with a ready shared organism.

## Preconditions

- The target/entry journey MUST exist.
- The shared organism MUST exist and be ready for use.
- Any required analytics migration MUST already be complete.

If the journey is missing, the Worker MUST return the task for target-journey migration. If required analytics are missing, the Worker MUST return the task for analytics migration. The Worker MUST not create the journey or add missing analytics in this job.

## Inputs

- The target journey and the old component rendering it replaces;
- The shared organism directory, local `index.ts`, and public export from `@shared/components/organisms`;
- `propsEngine` when the organism provides it;
- Content data, journey configuration, and approved differences; and
- The analytics migration report when analytics were required.

## Scope

The Worker MUST wire the ready shared organism into the existing journey. The Worker MUST NOT create a journey or implement analytics that are still missing.

## Process

1. Inspect the shared organism's local `index.ts` and the shared-organisms barrel. Import the organism through `@shared/components/organisms` and use its supported public API.
2. Inspect the old rendering only for the content, configuration, visual mode/layout, behavior, and ready analytics configuration that this migration must preserve.
3. Replace the old rendering with the shared organism. Map the journey data and configuration, using `propsEngine` when available.
4. Preserve the agreed visual mode, layout, user behavior, and ready analytics configuration. During journey migrations, use `io-mt-xl-*` for large-screen margin utilities; when replacing an existing `io-mt-lg-<number>` utility, retain its number and change only the breakpoint prefix to `io-mt-xl-<number>`. Record every approved difference.
5. Run the `report` Job. The Worker MUST maintain one living report for this logical task and update it in place for corrections.

## Output

The Worker report MUST include:

- the old-to-new component map;
- content and configuration mapping;
- the selected organism public API and import path;
- approved differences; and
- the scoped migration diff and verification results.

The output hands the migrated component in its entry journey to `components/verify-component-parity`. A Reviewer later checks the Worker evidence; the Reviewer does not own this job.
