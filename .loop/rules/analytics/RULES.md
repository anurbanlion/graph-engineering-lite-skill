# Analytics Rules

- Agents and Orchestrators MUST read the relevant documentation in `analytics/docs/` before implementing or reviewing analytics taggeos.
- When an implementation introduces an optional analytics prop on an organism component, agents MUST search for its direct production page renderers and configure the tracker at each applicable renderer before reporting the work complete. Storybook-only renderers MUST be excluded.
- Trackers for reusable or shared components MUST be defined and registered in the common schema registry with the common tracker namespace. Journey-specific registries MUST only contain trackers owned by that journey.
- When `TrackedAction` provides an interaction's analytics behavior, agents MUST remove any legacy callback prop and invocation whose only payload is tracking context and which has no remaining non-analytics consumer.
