# Dependency Workflow Algorithm

## Purpose

Create a reusable directed acyclic graph (DAG) that defines worker tasks, ownership, direct prerequisites, and deliverables for one orchestration flow. It is a template, not a Gantt schedule.

## Procedure

1. List the durable worker responsibilities required for one target area. For each responsibility, define its owned work and completion deliverables.
2. Assign each responsibility a unique worker number and kebab-case name. Keep tightly coupled substeps with one completion boundary in the same worker.
3. Add an edge from a producer to a consumer only when the consumer needs a concrete producer deliverable. Label the edge with that deliverable.
4. Identify per-target dependencies and global prerequisites. Per-target dependencies are copied when creating task instances; global prerequisites must be completed before each dependent instance starts.
5. Keep only direct edges. If `A -> B` and `B -> C`, omit `A -> C` unless `C` independently needs an output from `A` that `B` does not provide.
6. Validate that the graph is acyclic, that every required input has an incoming edge or documented global prerequisite, and that each nonterminal worker produces a meaningful output.

## Semantics

`A -> B` means that `B` may start only after `A` completes and provides the labeled output. Dependencies are transitive even when only direct edges are drawn. Independent workers have no path between them and may run in parallel when eligible.

## Mermaid

Use `flowchart TB`. Group owned substeps as `subgraph W<n> [Worker <n> — Responsibility]` with `direction TB`. Use stable node IDs such as `W1A`. Draw labeled edges between worker groups. Do not include target areas, dates, `T<n>`, status, or Gantt identifiers.

## Completion Check

The diagram is ready for Gantt scheduling only when every Gantt task can map to exactly one worker responsibility and one target area, without adding relationships absent from this diagram.
