# Migrate Analytics to a Shared Organism

## Description

Make an existing shared organism provide the analytics required by an existing old component.

## Preconditions

- The old component and the shared organism MUST both exist.
- The shared organism MUST be missing one or more required analytics behaviors.
- The Worker MUST receive the old component path and the shared organism path.

If a precondition is not met, the Worker MUST not change code. It MUST record the missing prerequisite in its living report and return it to the Orchestrator.

## Inputs

- The old component and its direct production callers;
- The shared organism and its public API;
- `.loop/rules/analytics/RULES.md` and the relevant files in `analytics/docs/`;
- Existing schemas, registries, and tracker registrations; and
- Any approved differences from the old analytics behavior.

## Scope

The Worker MUST add or reuse analytics in the shared organism and configure its direct production callers. The Worker MUST NOT wire the organism into a journey or create a target journey.

## Process

1. Read the analytics domain rules and `analytics/docs/` before making changes.
2. Audit the old component's user actions, event names, event data, and journey-level configuration. Add this audit to the same living Worker report; it MUST directly drive the implementation.
3. Search for a compatible existing schema. If none exists, define and register the required schema in the common registry for a reusable/shared organism.
4. Add the organism's supported optional `analytics` API. Its `TrackingTarget` context MUST contain only data the organism can provide.
5. Wire tracking with `TrackedAction` for clickable controls or `useTracking` for logic-driven events. Remove a legacy callback when its only purpose is to forward the same analytics data and it has no other consumer.
6. Find every direct production caller that must opt in and configure the required tracker. Storybook-only callers MUST be excluded.
7. Run the `report` Job. The Worker MUST maintain one living report for this logical task and update it in place for corrections.

## Output

The Worker report MUST include:

- the old-to-new event map, including explicit `none` for no analytics;
- schema and registry location;
- the organism analytics API and tracking wiring; and
- each required direct production caller and its tracker configuration.

The output hands off a shared organism that is ready for journey wiring. A Reviewer later checks the Worker evidence; the Reviewer does not own this job.

