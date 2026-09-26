# Worker Prompt Template

Use this structure for an orchestrator's initial prompt to a worker.

```markdown
## Task
State the assigned action and expected completion deliverable.

## Context
Provide only the relevant flow, dependency outputs, artifact documents, decisions, limits, and scope.

## Inputs
List the files, paths, values, prior outputs, and assigned Jobs required to perform the task.

## Required Reading
- `<flow-path>/workers/worker-<number>-<responsibility>/MEMORY.md` when it exists
- `<relevant-artifact-path>`
- `<assigned-job-path>/JOB.md`

## Completion
Return a concise completion message with the deliverables, validation performed, and any blocker.
```

Do not assign future Gantt tasks, unrelated Jobs, or unneeded repository context.
