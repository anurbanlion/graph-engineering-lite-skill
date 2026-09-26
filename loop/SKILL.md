---
name: loop
description: Use only when the user explicitly requests Loop or the Loop skill to create orchestration diagrams or execute dependency-driven multi-agent workspace flows.
---

# Loop

Use this skill to create orchestration diagrams and execute an isolated orchestration flow. Read the [workspace layout](README.md) before relying on repository configuration.

## Orchestration Diagram Creation

1. Understand the requested outcome, target areas, relevant `artifacts/` documents, and assigned Jobs.
2. Read [Dependency Workflow Algorithm](references/dependency-workflow-algorithm.md) and [Dependency Diagram Example](references/dependency-diagram-example.md), then create or revise the flow's `dependency-diagram.md`. The dependency diagram defines worker tasks, ownership, direct prerequisites, and the deliverables that unlock dependent work.
3. Do not create the Gantt diagram until the dependency diagram is valid. The dependency diagram is a reusable template; it MUST NOT contain target-area instances, dates, time units, task status, or worker-slot assignments.
4. Read [Gantt Scheduling Algorithm](references/gantt-scheduling-algorithm.md), then create or revise the flow's `gantt-diagram.md`. The Gantt diagram distributes eligible task instances across discrete time units.
5. The Gantt diagram MUST NOT introduce a worker, task ownership, prerequisite, or deliverable relationship that is absent from the dependency diagram.

## Execution Policy

Before scheduling or invoking workers, the orchestrator MUST read:

- `.loop/artifacts/RULES.md` and taks-relevant nested artifact documents;
- the selected flow's `dependency-diagram.md` and `gantt-diagram.md`; and
- the relevant Jobs from `.loop/jobs/`.

The dependency diagram defines task ownership and the outputs that unlock dependent work. The Gantt diagram defines execution order, priority, and the two scheduled tasks in each discrete time unit. Each worker in the dependency diagram is a distinct responsibility.

### Discrete Time Units

- Work runs in discrete time units: `T1`, `T2`, `T3`, and so on.
- Each unit invokes exactly the two tasks specified by its Gantt schedule.
- Both tasks in `Tn` MUST complete before `Tn + 1` may start.
- A worker that finishes early waits; it MUST NOT begin a future Gantt task early.
- By default, the orchestrator executes one time unit and then stops.
- The user MAY authorize multiple consecutive time units. The orchestrator MUST stop at the authorized limit.

### Worker Invocation and Memory

- The orchestrator MUST verify a task's dependencies before invoking its worker and provide only the assigned task, required inputs, relevant artifacts, and assigned Jobs.
- A worker is identified by `worker-<number>-<kebab-responsibility>`, never by a target area or a Gantt time unit.
- Before invoking a worker, the orchestrator MUST inspect the matching flow-local directory under `workers/`. If `MEMORY.md` exists, the worker MUST read and apply it.
- Read [Worker Memory Template](references/worker-memory-template.md) when creating or updating `MEMORY.md`. Memory records durable responsibility, corrections, rules, pointers, reusable patterns, and useful sources; it MUST NOT be an execution log.
- Read [Worker Prompt Template](references/worker-prompt-template.md) before sending a worker its initial task prompt.
- A flow MUST reuse the same persistent worker responsibility for later tasks that it owns. The `T<n>` label is only a scheduling and authorization boundary.
- Workers return a concise completion message when their assigned task is complete.

No reviewer or reformer is created or invoked during an execution phase. Review and audit work MAY instead be modeled as separate orchestration flows.
