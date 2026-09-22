# Verify Component Parity

## Description

Check that one migrated component and its shared-organism replacement behave as required in the relevant entry journey.

## Preconditions

- The old component and the new shared organism MUST both be identifiable in the relevant entry journey context.
- Relevant journey creation, analytics migration, and organism wiring MUST be complete.
- The Worker MUST receive the reports from the relevant earlier Worker jobs and any approved differences.

If evidence or a required earlier step is missing, the Worker MUST not report a pass. It MUST record the gap, return it to the Worker job that owns it, and rerun this same job after correction.

## Inputs

- Old component evidence in the entry journey;
- New shared organism evidence in the same entry journey;
- Relevant earlier Worker reports and the final diff;
- Approved differences; and
- `.loop/rules/analytics/RULES.md` and the relevant files in `analytics/docs/` when analytics are in scope.

## Scope

This job checks only the migrated component in its entry journey. It is a Worker-owned final job. It MUST NOT verify the whole journey, create a journey, migrate analytics, or act as the Reviewer.

## Process

1. Compare old and new component content and data.
2. Compare the intended visual mode and layout where they apply, except visual/style parity is out of scope for shared organisms that have Storybook coverage. For those organisms, verify functionality, data mapping, and equivalent tracking interactions/properties instead.
3. Compare user behavior and interactions.
4. When analytics are in scope, compare event names, sent event data, and journey-level configuration relevant to this organism.
5. Confirm every difference is explicitly approved. Do not require identical source code or identical pixels when the required result is preserved.
6. Return each gap to the Worker job that owns it. After correction, rerun this same parity job and update its existing report.
7. Run the `report` Job. The Worker MUST maintain one living report for this logical task and update it in place for corrections.

## Output

The Worker report MUST list each checked requirement, its evidence, approved differences, unresolved gaps, and a final `pass` or `changes required` result.

A Reviewer later checks whether the Worker performed this job correctly and whether the evidence supports its result. The Reviewer does not own the parity job.
