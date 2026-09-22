# Self-Improve Proposal - HeroBanner CTA analytics

These are outstanding proposals only. No Job or Rule file has been created or changed.

## Job Proposals

| Job name / path | Owner | When to run | Required inputs | Main work | Output / handoff | Limits |
| --- | --- | --- | --- | --- | --- | --- |
| [Migrate target journey](.loop/jobs/journeys/migrate-target-journey/JOB.md) | Worker | The target/entry journey does not exist and must be created or migrated from an old route before component wiring. | Old route or journey; required target App Router route; data/content source; journey shell and configuration requirements. | Create or migrate the route, journey shell, data loading, and journey-level configuration. Reuse/adapt the route-inventory structure from `.graph-engineering/runs/global/migrate-page-to-app-router/OUTPUT-20260826-1011.md` as a reference format, not as a reusable Job. | A living Worker report listing the legacy route, target App Router route, data/content source, journey shell status, and remaining component migrations. It hands the journey to the analytics job if needed, otherwise to organism wiring. | It does not assume a pre-existing Graph Engineering Job exists, that the shared organism is ready, or that component parity is complete. |

## Dependency Flow

```text
Migrate target journey
→ later work: migrate shared-organism analytics when needed
→ later work: wire the ready organism into the journey
→ later work: verify component parity
```

## Rule Proposals

| Domain | Proposed path | Rule purpose |
| --- | --- | --- |
| `analytics` | `.loop/rules/analytics/RULES.md` | Require the analytics job only when an old component and existing shared organism need equivalent analytics. The Worker must read `analytics/docs/`, use the common registry for shared-organism events, expose a supported analytics API, and configure required production callers. |
| `components` | `.loop/rules/components/RULES.md` | Require organism wiring to inspect `src/shared/components/organisms/<component>/`, its local `index.ts`, and `src/shared/components/organisms/index.ts`; import through `@shared/components/organisms`; and use the public API such as `propsEngine`. Require the final Worker parity job to compare the component only in its entry journey. |
| `journeys` | `.loop/rules/journeys/RULES.md` | Require target-journey migration before organism wiring when the entry journey is missing. The Worker must establish the route, journey shell, data, and journey-level configuration first. |
| `review` | `.loop/rules/review/RULES.md` | Require the Reviewer to check the Worker evidence and result for each assigned job, including component-parity evidence. The Reviewer does not own a migration or parity job. |

## Out of Scope

Possible future jobs—migrating a component with no analytics work, checking organism standards such as atom reuse, and creating stories—are not proposed here.
