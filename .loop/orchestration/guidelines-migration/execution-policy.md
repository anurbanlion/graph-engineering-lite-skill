# Execution Policy

## Read First

Before scheduling or invoking workers, the orchestrator MUST read:

- [Dependency Diagram](./dependency-diagram.md)
- [Dependency Diagram Algorithm](./dependency-diagram-algorithm.md)
- [Gantt Diagram](./gantt-diagram.md)
- [Gantt Scheduling Algorithm](./gantt-scheduling-algorithm.md)

## Sources of Truth

- The [Dependency Diagram](./dependency-diagram.md) defines task ownership and the outputs required to unlock dependent work.
- The [Dependency Diagram Algorithm](./dependency-diagram-algorithm.md) defines how to construct and validate the dependency template.
- The [Gantt Diagram](./gantt-diagram.md) defines execution order, priority, and the two workers assigned to each discrete time unit.
- Each worker shown in the dependency diagram is a distinct worker responsibility.

## Execution by Discrete Time Units

- Work runs in discrete time units: `T1`, `T2`, `T3`, and so on. Each unit corresponds to the pair of tasks scheduled at the same logical time in the Gantt diagram.
- Each time unit invokes exactly the two workers specified by its Gantt schedule.
- Both workers in `Tn` MUST complete before `Tn + 1` may start.
- A worker that finishes early waits; it MUST NOT begin a future Gantt task early.
- By default, the orchestrator executes one time unit and then stops.
- The user MAY explicitly authorize multiple consecutive time units. The orchestrator MUST stop when it reaches the user-authorized limit.

## Worker Invocation

- For every scheduled task, the orchestrator provides the worker with only its assigned task, required inputs, relevant rules, and assigned jobs.
- The orchestrator MUST verify that the task's dependencies from the dependency diagram are complete before invoking its worker.
- Before invoking a worker for the first time in an orchestration, the orchestrator MUST inspect `.loop/orchestration/guidelines-migration/` for an existing directory named `worker-<number>-<kebab-responsibility>`, using the worker number and responsibility defined in the dependency diagram.
- If that worker directory contains a `MEMORY.md`, the orchestrator MUST instruct the worker to read it before starting work and apply its durable lessons.
- Worker memory directories MUST use the format `worker-<number>-<kebab-responsibility>`; a Gantt time unit MUST NOT be used in the directory name. The route-shell task formerly labeled `T1 route shell` belongs to Worker 6 and MUST use the Worker 6 identity and memory directory.
- Worker memory MAY record lessons, commands, snippets, jobs, and consulted documents, but the dependency diagram MUST NOT be modified by a worker unless the orchestrator or user explicitly requests that change.
- Worker memory MUST describe the worker's durable responsibility, corrections, rules, pointers, reusable patterns, and useful sources; it MUST NOT become a historical execution report listing completed, incomplete, or non-applicable work.
- Worker memory and worker completion messages MUST be written in English unless the user explicitly requests another language.
- The orchestrator MUST NOT create a new subagent solely to populate a worker memory `MEMORY.md`. Memory updates MUST reuse an existing worker or be deferred until that worker has real execution experience.
- Workers return a concise completion message to the orchestrator when their assigned task is complete.
- Each dependency-diagram worker responsibility MUST have one persistent subagent for the migration.
- The orchestrator MUST name each subagent after its worker number and owned responsibility, never after a target organism or Gantt time unit.
- The orchestrator MUST reuse that same subagent for every later task owned by its worker responsibility.
- The Gantt time unit (`T1`, `T2`, and so on) MUST be used only for scheduling and authorization boundaries; it MUST NOT appear in a subagent name.

Examples:

```text
w1_organism_contract
w2_fixtures_and_storybook
w6_new_journey
```

## Current Exclusions

- No reviewer or reformer is created or invoked during this execution phase.
