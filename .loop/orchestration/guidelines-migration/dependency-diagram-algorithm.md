# Dependency Diagram Algorithm

## Purpose

The dependency diagram is the reusable workflow template for an orchestration. It defines worker responsibilities, their owned work, the direct prerequisites between responsibilities, and the deliverables that unlock later work.

It is not a Gantt schedule. It MUST NOT contain target-area instances, time units such as `T1`, dates, execution history, worker-slot assignments, or task status. The Gantt Scheduling Algorithm instantiates this template once per target area and schedules those instances.

## Inputs

Build or revise the diagram from:

- the requested outcome and target areas;
- reusable Rules and assigned Jobs;
- the deliverables each responsibility must produce or consume; and
- real technical constraints, including global prerequisites.

A worker represents one durable responsibility, not a target area, an individual task, or a Gantt time unit. Give every worker a unique number and a short kebab-case responsibility that can also form its persistent memory-directory name: `worker-<number>-<kebab-responsibility>`.

## Construction Algorithm

1. List the durable responsibilities needed to complete one target area. For each one, state its owned work and its completion deliverables.
2. Assign one worker to each responsibility. Keep tightly coupled substeps that share one completion boundary inside that worker; do not split them into artificial workers merely to make the diagram more granular.
3. For every responsibility, identify the minimum direct predecessors whose deliverables it actually needs. Add a directed edge from each producer to that consumer, labeling the edge with the delivered artifact or capability.
4. Classify each dependency as either per-target or global. A per-target edge is copied when the template is instantiated for each target area. A global prerequisite is represented explicitly and must be complete before every dependent instance can begin.
5. Reduce the graph to direct dependencies. If `A -> B` and `B -> C`, do not add `A -> C` unless `C` independently needs an artifact from `A` that `B` does not provide. The resulting diagram MUST preserve reachability while avoiding redundant edges.
6. Validate that the graph is a directed acyclic graph (DAG). A worker MUST NOT directly or indirectly depend on itself. Resolve a cycle by changing ownership, splitting an invalidly coupled responsibility, or introducing a real prerequisite boundary; never hide it by omitting an edge.
7. Check completeness: every non-root responsibility has all of its required inputs represented by incoming edges or documented global prerequisites, and every nonterminal responsibility has a meaningful deliverable or consumer.
8. Review the diagram with the target-area workflow in mind. A path through the graph must describe a feasible order from initial inputs to an integrated outcome. Only after this validation may the Gantt Scheduling Algorithm create task instances and time units.

## Dependency Semantics

An edge `A -> B` means that `B` MAY start only after `A` completes and provides the labeled output. It does not mean that `A` and `B` happen in adjacent time units, share a target area in the schedule, or use the same subagent.

Dependencies are transitive: if `A -> B` and `B -> C`, then `C` is transitively dependent on `A`. The diagram normally draws only the direct edges, while scheduling and validation MUST honor the full transitive closure. A task is eligible only when all direct and therefore all transitive prerequisites for its instance are complete.

Independent workers have no path between them and MAY be scheduled in parallel when eligible. A dependency is not inferred from worker numbering, visual placement, a similar name, or a shared target area; it must be represented by an edge or a documented global prerequisite.

## Mermaid Authoring Rules

Use a Mermaid `flowchart TB` for the dependency diagram.

- Group each worker's internal substeps in `subgraph W<n> [Worker <n> — Responsibility]` with `direction TB`.
- Use stable, unique node identifiers such as `W1A`, `W1B`, and descriptive action-oriented labels. Internal arrows show the owned sequence within one worker.
- Draw inter-worker dependencies between worker subgraphs and label each arrow with the concrete output that unlocks the consumer, for example `W1 -->|"props and propsEngine"| W2`.
- Keep the graph template-oriented: use worker and deliverable names, never target-area names, `T<n>`, dates, `done`, or Gantt task identifiers.
- Prefer top-to-bottom flow and a small number of direct, labeled cross-worker edges. Do not use visual layout to convey a dependency that is absent from the graph.
- A worker with one atomic responsibility MAY have one node; it still requires a worker subgraph when the surrounding diagram uses worker groupings.

## Pre-Scheduling Validation

Before generating or accepting a Gantt diagram, verify:

- worker numbers, responsibilities, and memory-directory identities are unique;
- every edge has a producer, consumer, and meaningful output label;
- every consumer's listed inputs have a direct predecessor or an explicit global prerequisite;
- the graph is acyclic and its transitive dependencies are satisfiable;
- no redundant transitive edge obscures the direct dependency structure; and
- each Gantt task can be mapped to exactly one worker responsibility and one target area.

When the workflow changes, update the dependency diagram first, then regenerate or revise the Gantt diagram using the Gantt Scheduling Algorithm. The schedule MUST NOT silently introduce a worker, prerequisite, or ownership relationship absent from the dependency template.
