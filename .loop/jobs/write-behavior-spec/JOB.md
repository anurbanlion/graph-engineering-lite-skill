# Write Behavior Spec

## Input

- The target journey name;
- The feature name;
- The target rule or behavior to create or edit;
- User-provided behavior information, in any combination of prose, scenarios, images, mocks, existing specifications, or other reference material.

## References

- `.loop/artifacts/specs/catalog-journey/product-search.spec.md` is the reference
  format for a behavior specification.

## Process

1. Determine the target specification path. Create the journey folder, feature specification, feature, or rule when the requested behavior does not yet exist.
2. Read only the supplied information and relevant referenced artifacts needed to understand the requested behavior.
3. Create or edit the requested rule and its scenarios. Preserve the meaning, scope, and distinctions in the supplied information. Write the specification in English; do not add requirements, summarize scenarios, or reinterpret behavior.
4. Follow the reference format using `Feature`, `Rule`, and `Scenario` with `Given`, `When`, and `Then` statements.
5. Do not include implementation details such as APIs, services, data stores, routes, components, handlers, or technical architecture unless they were explicitly supplied as observable behavior.
6. Save the specification at `.loop/artifacts/specs/<journey-kebab-case>/<feature-kebab-case>.spec.md`.

## Output

One created or updated behavior specification at `.loop/artifacts/specs/<journey-kebab-case>/<feature-kebab-case>.spec.md`.
