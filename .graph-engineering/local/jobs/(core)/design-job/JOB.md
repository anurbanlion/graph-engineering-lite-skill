# Design Job V2

## Objective

The job MUST design, validate, and materialize an executable local job as Project Outputs under `.graph-engineering/local/jobs/<job-identifier>/`.

The job MUST support jobs based on `JOB.md` and graph jobs based on `GRAPH.json`.

The job MUST NOT produce a Managed Output.

The job MUST NOT integrate generated jobs into the canonical skill job or graph stores.

## Inputs

The job MAY receive any combination of the following optional inputs, including none of them:

- A proposed job identifier;
- A proposed human-readable title;
- A proposed `job_group_path`, using `.` for no group or slash-separated kebab-case segments for nested groups;
- A preferred process format of `job` or `graph`;
- The job's objective;
- The job's expected inputs;
- The job's expected Project Outputs;
- The job's process;
- The job's requirements and constraints;
- Final script names and requested script behavior;
- An existing draft, graph, or legacy job definition;
- Prior conversation or design notes;
- An explicit overwrite decision when the target local job already exists.

Examples:

```txt
Execute design-job-v2 to create a local graph job named compile-initiatives.
```

```txt
Execute design-job-v2 to design and materialize a local JOB.md-based job from these requirements: [requirements].
```

## Scope

The agent MAY inspect:

```txt
<local-skill-folder>/graph-engineering/templates/job-template.md
<local-skill-folder>/graph-engineering/jobs/**/JOB.md
<local-skill-folder>/graph-engineering/jobs/**/GRAPH.json
<local-skill-folder>/graph-engineering/graphs/**/GRAPH.json
.graph-engineering/local/jobs/**
```

The agent MAY modify:

```txt
.graph-engineering/local/jobs/<job-identifier>/JOB.md
.graph-engineering/local/jobs/<job-identifier>/GRAPH.json
.graph-engineering/local/jobs/<job-identifier>/GRAPH.md
.graph-engineering/local/jobs/<job-identifier>/scripts/**
```

The agent MUST NOT modify the following unless the user explicitly requests it:

```txt
<local-skill-folder>/graph-engineering/jobs/**
<local-skill-folder>/graph-engineering/graphs/**
```

## Process

1. The agent MUST execute the state machine defined in `GRAPH.json`.

## Output

The job MUST produce Project Outputs only and MUST NOT produce a Managed Output.

The Project Outputs MUST be materialized beneath:

```txt
.graph-engineering/local/jobs/<job-identifier>/
├── JOB.md
├── GRAPH.json
├── GRAPH.md
└── scripts/
    └── <final-script-name>.<extension>
```

A `JOB.md`-based generated job MUST include `JOB.md` and MAY omit `GRAPH.json` and `GRAPH.md`.

A graph-based generated job MUST include a valid `GRAPH.json`, a synchronized `GRAPH.md`, and an auxiliary `JOB.md` when required by the execution runtime.

Every creation or modification of a generated `GRAPH.json` MUST be followed by execution of `.graph-engineering/local/scripts/graph_to_mermaid.py` before graph review or validation.

Generated scripts MUST retain the final names, extensions, and local references confirmed during the design.

Output generation, validation, and materialization are orchestrated by `GRAPH.json`.

**Context Output Extension**

In addition to mandatory Project Output links, the Context Output MUST report:

- The final job identifier and title;
- The generated format;
- Every created or modified local artifact;
- Every generated script;
- Validation warnings or relevant design decisions;
- A realistic example for executing the local job.

On failure, the agent MUST report the failing state, validation error, conflict decision, or materialization error without leaving a partial local job.

## Prompt examples

```txt
Execute design-job-v2 to create a local graph job named compile-initiatives that reads project notes and compiles initiative summaries.
```

```txt
Execute design-job-v2 to create a local JOB.md-based job from the following objective, inputs, outputs, and process: [design context].
```
