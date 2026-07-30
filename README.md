# Graph Engineering Lite Skill

A lightweight GitHub-hosted skill for defining, validating, and executing reusable **jobs** and **graphs** through a clear, file-based workflow.

The repository centers on the `job-graph-engineering` skill, which lets an agent discover available jobs or graphs, select the best match for an explicit user request, validate graph definitions, execute the referenced workflow, and write outputs to deterministic project paths.

## What this project provides

- A convention for reusable jobs stored as `JOB.md` files.
- A convention for workflow graphs stored as graph definitions.
- Scripts for listing, reading, and validating jobs and graphs.
- Deterministic output-path resolution for generated artifacts.
- Execution logging under the consuming project's `logs` directory.
- Guardrails that require explicit user intent before creating or running jobs and graphs.

## Repository structure

```text
job-graph-engineering/
├── SKILL.md
├── graphs/
│   └── <graph-name>/
│       └── GRAPH.json
├── jobs/
│   └── <job-name>/
│       └── JOB.md
└── scripts/
    ├── list-jobs.mjs
    ├── read-jobs.mjs
    ├── list-graphs.mjs
    ├── read-graphs.mjs
    ├── validate-graph.mjs
    ├── resolve-output-path.mjs
    └── lib/
```

Generated outputs are resolved inside the consuming project using a structure similar to:

```text
<project-folder>/
├── logs/
│   └── executions.log
└── runs/
    └── <domain>/
        └── <job-name>/
            └── <output-file>
```

## Requirements

- Node.js with ES module support.
- A project root from which the skill scripts can be executed.
- Explicit user intent before a job or graph is created or executed.

## Working with jobs

List the available jobs from the project root:

```bash
node job-graph-engineering/scripts/list-jobs.mjs
```

Read the selected job definition:

```bash
node job-graph-engineering/scripts/read-jobs.mjs <job-name>
```

Before writing a job output, resolve the exact destination path:

```bash
node job-graph-engineering/scripts/resolve-output-path.mjs <domain> <job-name>
```

Jobs are selected by name before their definitions are read. Each job lives in its own directory and defines its workflow in `JOB.md`.

## Working with graphs

List the available graphs:

```bash
node job-graph-engineering/scripts/list-graphs.mjs
```

Read a selected graph:

```bash
node job-graph-engineering/scripts/read-graphs.mjs <graph-name>
```

Validate a graph before execution:

```bash
node job-graph-engineering/scripts/validate-graph.mjs 1.0 <graph-name>
```

A graph defines an initial job, job-specific instructions, success transitions through `onDone`, and failure transitions through `onError`. Terminal outcomes are `complete` and `abort`.

## Execution model

1. Receive an explicit user request.
2. List the available jobs or graphs.
3. Select the single best match by name.
4. Read only the selected definition.
5. Validate the graph when applicable.
6. Resolve the output path when the selected job produces a file.
7. Execute the workflow and follow its transitions.
8. Record outputs and execution activity in the consuming project.

## Design principles

- **Explicit execution:** nothing runs without a direct user request.
- **Discover before reading:** available names are listed before a definition is selected.
- **Deterministic outputs:** scripts resolve output locations instead of relying on ad hoc paths.
- **Composable workflows:** graphs coordinate reusable jobs without duplicating each job's internal process.
- **Fail clearly:** invalid graph references or failed validation stop execution before downstream work begins.

## Current scope

This repository provides the core conventions, scripts, and example job definitions for lightweight graph-based orchestration. It is intentionally small and file-driven so that workflows remain easy to inspect, version, review, and extend.

## Contributing

When adding a job, create a dedicated directory containing a `JOB.md` definition and use RFC-style normative language for requirements. When adding a graph, ensure every referenced job exists and validate the graph before submitting changes.
