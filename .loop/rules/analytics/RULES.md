# Analytics Rules

- Agents and Orchestrators MUST read the relevant documentation in `analytics/docs/` before implementing or reviewing analytics taggeos.
- When an implementation introduces an optional analytics prop on an organism component, agents MUST search for its direct production page renderers and configure the tracker at each applicable renderer before reporting the work complete. Storybook-only renderers MUST be excluded.
- Trackers for reusable or shared components MUST be defined and registered in the common schema registry with the common tracker namespace. Journey-specific registries MUST only contain trackers owned by that journey.
- When `TrackedAction` provides an interaction's analytics behavior, agents MUST remove any legacy callback prop and invocation whose only payload is tracking context and which has no remaining non-analytics consumer.

## Organism analytics readiness

- Before journey migration, the Worker MUST identify every perceptible organism interaction: a visible control a user can click, open, select, play, submit, or otherwise operate.
- An organism with no perceptible interaction MUST be recorded as analytics `none` and is ready for journey migration.
- An organism with perceptible interactions is ready only when its public props expose optional action-specific `analytics` targets, its organism-level wiring uses a named `useTracking` handler or `TrackedAction` as applicable, every target exists in the registered schema registry, and every applicable direct production renderer configures that target.
- The Worker MUST treat legacy tracking callbacks such as `onTrack...`, `onClick...`, or `on...Clicked` that forward analytics context as evidence that analytics migration is still required.
- The Worker MUST treat direct legacy tracker calls, analytics-context callbacks passed into molecules, and interactive controls that do not reach `useTracking` or `TrackedAction` as evidence that analytics migration is still required.

### Ready analytics API

```ts
type FeaturesStepsProps = {
  analytics?: {
    stepClicked?: TrackingTarget<FeaturesStepsStepClickedContext>;
    ctaClicked?: TrackingTarget<FeaturesStepsCtaClickedContext>;
  };
};
```

```ts
// Not ready: legacy tracking callback owned by the caller.
onTrackStepClick?: (context: Record<string, unknown>) => void;
```

The legacy callback is not server-render friendly because the parent must pass a function. A ready organism instead receives serializable tracker configuration through `analytics`; the organism owns the runtime context and sends the event internally.

```tsx
// Not ready: the page must pass a tracking function.
<FeaturesSteps onTrackStepClick={trackLegacyStepClick} />

// Ready: a Server Component can pass a registered ID or a disabled configuration object.
<FeaturesSteps
  analytics={{
    stepClicked: "common.featuresStepsStepClicked",
    ctaClicked: { id: "common.ctaClicked", disabled: true },
  }}
/>
```

### Ready organism wiring

The organism, not a molecule, MUST map generic interaction data to analytics context. Logic-driven interactions use a named handler and `useTracking`; an organism-exposed CTA uses `TrackedAction`.

```tsx
const handleStepOnClick = (step: Step) => {
  track(analytics?.stepClicked, { option: step.title });
};

<FeaturesStep onClick={() => handleStepOnClick(step)} />
```

```tsx
<TrackedAction tracking={analytics?.ctaClicked} context={{ option: cta.label }}>
  <LDButton>{cta.label}</LDButton>
</TrackedAction>
```

### Ready renderer configuration

Every configured target MUST exist in the registered analytics schema registry. Reusable organism targets belong in the common namespace, and every applicable direct production renderer configures the supported slot.

```tsx
<FeaturesSteps
  analytics={{ stepClicked: "common.featuresStepsStepClicked" }}
/>
```

| Result | Meaning | Next owner |
| --- | --- | --- |
| Ready with analytics | Props, wiring, registered targets, and applicable renderers are complete. | Journey migration job |
| Ready: `none` | No perceptible interaction exists. | Journey migration job |
| Not ready | Any required API, wiring, schema, or renderer configuration is missing. | Analytics migration job |
