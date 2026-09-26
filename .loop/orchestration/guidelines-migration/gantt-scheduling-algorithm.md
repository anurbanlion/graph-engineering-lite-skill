# Gantt Scheduling Algorithm

## Core Model

A dependency diagram defines a reusable **workflow template**. A worker is a responsibility in that template; it is not, by itself, a Gantt node.

A Gantt task is an instantiation of one worker responsibility for one target area. For example:

```text
Worker 1: Contract
Target area: Area A
Gantt task: Contract(Area A)
```

The same workflow can be instantiated for `Area A`, `Area B`, and `Area C`. Therefore, `Contract(Area A)`, `Contract(Area B)`, and `Contract(Area C)` are separate Gantt tasks even though they use the same worker responsibility.

## Eligibility

- A task is eligible only when every predecessor task for the same target area is complete.
- A task with a global prerequisite is eligible only when that global prerequisite is complete as well.
- The orchestrator creates task instances from the dependency template and the requested target areas; workers do not construct or manage the schedule themselves.

## Breadth-First Scheduling

1. Build the task graph by instantiating the dependency template once per target area.
2. Start with every task that has no incomplete prerequisite.
3. Select tasks from the shallowest available dependency layer first.
4. When a time unit has a free worker slot after selecting all available tasks at that layer, fill it with the next eligible task from the following layer.
5. When tasks have the same dependency layer, use the target-area order established by the Gantt as the tie-breaker.
6. Put exactly two selected tasks into each discrete time unit.
7. Do not advance to the next time unit until both selected tasks finish and the user authorizes continuation.

This is breadth-first search (BFS) over **task instances**, not over worker names.

## Small Dependency Template Example

```mermaid
flowchart LR
    W1["Worker 1<br/>Create contract"] --> W2["Worker 2<br/>Create fixtures"]
    W1 --> W3["Worker 3<br/>Create flat implementation"]
    W2 --> W4["Worker 4<br/>Publish"]
    W3 --> W4
```

For each target area, the template becomes this task dependency graph:

```mermaid
flowchart LR
    A1["Contract<br/>Area A"] --> A2["Fixtures<br/>Area A"]
    A1 --> A3["Implementation<br/>Area A"]
    A2 --> A4["Publish<br/>Area A"]
    A3 --> A4

    B1["Contract<br/>Area B"] --> B2["Fixtures<br/>Area B"]
    B1 --> B3["Implementation<br/>Area B"]
    B2 --> B4["Publish<br/>Area B"]
    B3 --> B4

    C1["Contract<br/>Area C"] --> C2["Fixtures<br/>Area C"]
    C1 --> C3["Implementation<br/>Area C"]
    C2 --> C4["Publish<br/>Area C"]
    C3 --> C4
```

## BFS Gantt Example

With two workers per time unit, the following Gantt is a breadth-first schedule for the three-area graph above. Publication tasks wait while eligible contract, fixture, or implementation tasks remain at shallower layers.

```mermaid
gantt
    title BFS example — three target areas, two workers per time unit
    dateFormat  YYYY-MM-DD
    axisFormat  %d

    section Area A
    T1 — Contract                                  :aContract, 2026-01-01, 1d
    T2 — Fixtures                                  :aFixtures, 2026-01-02, 1d
    T3 — Flat implementation                       :aImplementation, 2026-01-03, 1d
    T5 — Publish                                   :aPublish, 2026-01-05, 1d

    section Area B
    T1 — Contract                                  :bContract, 2026-01-01, 1d
    T3 — Fixtures                                  :bFixtures, 2026-01-03, 1d
    T4 — Flat implementation                       :bImplementation, 2026-01-04, 1d
    T6 — Publish                                   :bPublish, 2026-01-06, 1d

    section Area C
    T2 — Contract                                  :cContract, 2026-01-02, 1d
    T4 — Fixtures                                  :cFixtures, 2026-01-04, 1d
    T5 — Flat implementation                       :cImplementation, 2026-01-05, 1d
    T6 — Publish                                   :cPublish, 2026-01-06, 1d
```

The first publication, `Publish(Area A)`, is scheduled only after every eligible shallower task that could fill earlier time units has been dispatched. The same algorithm scales to any number of workflow targets without changing the dependency template.
