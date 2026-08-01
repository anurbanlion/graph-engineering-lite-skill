# [Job Title]

> Location: `graph-engineering/jobs/<job-name>/JOB.md`  

> Note: The job directory name MUST be a kebab-case identifier (e.g., `analyze-journey-use-cases`). The document heading SHOULD be the human-readable title of that identifier.

## Objective

The job MUST [define the job's responsibility and target outcome].

The job MUST NOT [state explicit non-goals, out-of-scope operations, or boundaries, ONLY when necessary].

## Inputs

The job MUST receive:

- [required input];
- [required input].

> Note: Inputs may originate from user parameters, previous job artifacts, explicit source or media files, or workspace discovery.

The job MAY receive:

- [optional constraint, context, or `domain` parameter].

> Note: When producing or consuming domain-bound artifacts, the job MUST receive a kebab-case domain identifier.

## Scope (Optional)

> Note: Include this section only when file inspection, mutation, or protection paths require strict boundaries.

The agent MAY inspect:

```txt
[allowed/path]
```

The agent MAY modify:

```txt
[allowed/output/path]
```

The agent MUST NOT modify the following unless the user explicitly requests it:

```txt
[protected/path]
```

> Note: Omit unnecessary path constraints; defining protected paths or write boundaries is sufficient for most scoped jobs.

## Process

> Note: Simple jobs MAY use a linear sequential workflow. Jobs requiring exploration, state synthesis, implementation, or verification SHOULD structure execution into ordered named stages. The process MUST specify deterministic operations, decision criteria, and operational boundaries, and MUST NOT document internal cognitive reasoning.

### Option A: Short Ordered Sequence (Simple Job)

1. The agent MUST [first operation].
2. The agent MUST [second operation].
X. The agent MUST [final operation or validation step].

### Option B: Named Stages (Complex Job)

**1. [Stage Name]**

1. The agent MUST [operation, decision, or validation step for this stage]
2. The agent MUST [second operation].
X. The agent MUST [final operation or validation step].
## Output

The job MUST produce [deliverable specification: e.g., persisted Markdown artifact or repository source code].

Output serialization and formatting are executed [manually by the agent / deterministically by script].

> Note: Include representative output schemas or structural examples below matching the job deliverables.

**Markdown Document Output (when applicable)**

```md
# [Output Title]

[Example table, section structure, or output content]
```

### Code / Directory Structure Output (when applicable)

```txt
[generic/path/to/output/files]
└── [example-file.ts]
```

On successful completion, the agent MUST report:

- [completed unit, artifact location, file link, or execution summary];
- [changes, findings, or handoff values].

On failure, the agent MUST report [error context, failing input, missing dependency, or target path].

## Prompt examples

```txt
[concise user prompt triggering this job]
```

```txt
[secondary prompt demonstrating contextual execution or parameters]
```
