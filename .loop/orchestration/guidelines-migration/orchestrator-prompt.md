# Prompt for the Guidelines Migration Orchestrator

You are the orchestrator for the **Preguntas Frecuentes** migration.

## Read First

Read these resources completely before taking any action:

1. `.codex/skills/loop/SKILL.md`
2. `.graph-engineering/artifacts/routes-components-checklist.md`
3. Every file in `analytics/docs/`
4. `openspec/specs/components-conventions/design.md`
5. Every relevant job under `.loop/jobs/`
6. The local orchestration artifacts in `.loop/orchestration/guidelines-migration/`:
   - `dependency-diagram.md`
   - `gantt-diagram.md`
   - `execution-policy.md`
   - `gantt-scheduling-algorithm.md`

## Objective

Migrate the **Preguntas Frecuentes** journey. The legacy page is reference-only and MUST NOT be modified. Reuse existing organisms where available, create full organisms where absent, add required analytics support, and integrate the resulting organisms into the new journey.

`Navbar`, `PreFooterBanner`, and `Footer` are already available as organisms with Storybook coverage and analytics tagging, as established by the checklist. They do not enter the organism-creation workflow. They are integrated when the new journey route shell is created.

`HeroBannerSearch`, `QuestionsAndAnswers`, and `ContactCard` MUST go through the dependency-diagram workflow and be scheduled through the Gantt diagram. These are the components that require the contract, fixtures/Storybook, flat-organism, analytics, publication, and journey-integration flow.

Use this target checklist verbatim as the migration scope:

```md
# Preguntas Frecuentes

- Ruta antigua: [pages/preguntas-frecuentes.tsx](../../pages/preguntas-frecuentes.tsx)
- Ruta nueva: [app/(landing-page)/preguntas-frecuentes/page.tsx](../../app/(landing-page)/preguntas-frecuentes/page.tsx)

| Componente Original   | Componente Migrado | Storybok | Taggeos |
| --------------------- | ------------------ | -------- | ------- |
| `NavBar`              |                    |          |         |
| `HeroBannerSearch`    |                    |          |         |
| `QuestionsAndAnswers` |                    |          |         |
| `ContactCard`         |                    |          |         |
| `PreFooterBanner`     |                    |          |         |
| `Footer`              |                    |          |         |
```

## Constraints

- Do not use any OpenSpec skill or workflow.
- Read the Loop skill and its relevant jobs, but ignore the Loop skill's agent-execution, reviewer, reformer, and reporting mechanics for this migration.
- Follow `execution-policy.md` and `gantt-diagram.md` instead.
- Do not create a reviewer, reformer, review queue, or worker reports.
- Workers MUST NOT write reports. They return only concise completion messages to the orchestrator.
- Execute only the time unit explicitly requested by the user. After its two workers complete, stop and wait for the user to authorize the next time unit.
- Use the dependency diagram and Gantt diagram as the source of truth for task ownership, prerequisites, and scheduling.

Once you are done reading and understanding the material, ask the user if you can proceed by invoking the corresponding subagents.
