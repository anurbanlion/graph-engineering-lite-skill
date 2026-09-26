# Worker 4 — Organism Analytics

## Responsibility

Worker 4 owns reusable organism analytics. For each assigned organism, audit the
direct legacy interaction and expose only supported optional `TrackingTarget` slots
in the organism contract. Keep tracking and payload adaptation inside the organism;
routes supply tracker configuration only. Legacy pages are reference-only.

## Authoritative references

- `.loop/artifacts/RULES.md`
- `.loop/orchestration/guidelines-migration/dependency-diagram.md`
- `loop/SKILL.md`
- `analytics/docs/`
- `analytics/schemas/index.ts` and `analytics/globalRegistry.ts`

The dependency diagram assigns W4 organism analytics. W1 contracts, W2
fixtures/Storybook, W3 flat-organism/publication, and W7 route integration have
separate ownership.

## Durable rules

- Only IDs registered in `analytics/schemas` and the global registry are valid.
- Use `TrackingTarget` only for interaction slots provided by the component.
- Prefer a compatible common schema; add a journey-specific schema only when the
  exact legacy payload is genuinely component-specific.
- CTA events use `ctaClicked`; other events use semantic `Clicked` or `Opened`
  names.
- Use `TrackedAction` for a directly clickable control. Use `useTracking` and a
  named handler for logic-driven events. Never call `track(...)` inline in JSX.
- Molecules emit neutral scalar values. They MUST NOT import an analytics context
  from an organism or pass an opaque analytics context upward. The organism adapts
  these values to its tracker context immediately before tracking.
- When an organism receives plain and rich text for a textual payload value, derive
  it with `getTextFromPlainOrRichText(plainValue, richValue)`.
- Preserve `IoLink` navigation, visual mode, responsive/alignment classes, and the
  text guard when simplifying a CTA component.
- Do not invent events for static content or imperceptible interactions.
- Do not modify legacy sources, route-level implementation, dependency/Gantt
  diagrams, reports, reviewer/reformer artifacts, or another worker's scope.

## Reusable patterns

Direct CTA tracking:

```tsx
<TrackedAction tracking={analytics?.ctaClicked} context={context}>
  <LDButton mode="dark" {...button}>{buttonText}</LDButton>
</TrackedAction>
```

Logic-driven tracking adapted in the organism:

```tsx
const handleAction = (option: string, section?: string) => {
  track(analytics?.actionClicked, { option, section } satisfies ActionContext);
};
```

## Useful queries and validation

```powershell
rg -n -F 'TrackerOrEventName' analytics src app pages -g '*'
rg -n -F 'organism-name' src app -g '*'
git -c core.autocrlf=false -c core.whitespace=cr-at-eol diff --check
```

Always use the exact validation command above; it avoids CRLF false positives.

## Pitfalls

- Retaining a CTA molecule that only forwards `onClick` and tracking. Render the
  button under `TrackedAction` in the organism instead, moving an essential style
  into the organism module.
- Renaming registered IDs without updating code references and removing obsolete
  registry keys.
- Choosing only a plain title when rich text is also available.
- Introducing an upward molecule-to-organism import for a callback type.
- Overwriting concurrent shared-workspace changes rather than working around them.

## Handoff checklist

- [ ] Compare the direct legacy interaction and exact legacy payload.
- [ ] Check schemas and the global registry for a compatible registered target.
- [ ] Keep analytics optional in organism props and use semantic target names.
- [ ] Keep tracking and payload construction in the organism.
- [ ] Verify molecule callbacks are neutral and dependency direction is correct.
- [ ] Preserve rich-text extraction and declarative link navigation.
- [ ] Confirm all changes remain within W4 scope.
- [ ] Run the required CRLF-safe diff validation.
