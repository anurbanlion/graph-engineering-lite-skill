# [Job Title]

> Version: 1.0

> Location: `graph-engineering/jobs/<job-name>/JOB.md`  

> Note: The job directory name MUST be a kebab-case identifier (e.g., `analyze-journey-use-cases`). The document heading SHOULD be the human-readable title of that identifier.

> Note: Lines starting with `>` are template instructions and guidelines. They MUST NOT be included in the final generated `JOB.md` file.

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

Examples:

```txt
[input examples]
```

## Scope (Optional)

> Note: Include this section only when file inspection, mutation, or protection paths require strict and explicit boundaries.

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

> Note: Omit unnecessary path constraints; defining protected paths or write boundaries MAY be sufficient for most scoped jobs.

## Process

> Note: Simple jobs MAY use a linear sequential workflow. Jobs requiring exploration, state synthesis, implementation, or verification SHOULD structure execution into ordered named stages. The process MUST specify deterministic operations, decision criteria, and operational boundaries, and MUST NOT document internal cognitive reasoning. There is no limit on the number of steps, but as a general rule we should aim to less than 15 steps.

[Option A: Short Ordered Sequence (Simple Job)*]

1. The agent MUST [first operation].
2. The agent MUST [second operation].
3. The agent MUST [final operation or validation step].

- Additional notes or rules to the process for complex job

[Option B: Named Stages (Complex Job)]

**1. [Stage Name]**

1. The agent MUST [operation, decision, or validation step for this stage]
2. The agent MUST [second operation].
3. The agent MUST [final operation or validation step].

- Additional notes or rules to the process for complex job

## Output

The job MUST produce [deliverable specification: Project Output (repository files/code), Managed Output (persisted Markdown artifact), or both]. Every successfully completed job produces the skill-defined Context Output.

Output generation, serialization and formatting are executed [manually by the agent / deterministically by script].

> Note: Include representative output schemas or structural examples below matching the job deliverables.

**Markdown Document Output (when applicable)**

```md
# [Output Title]

[Example table, section structure, or output content]
```

**Code / Directory Structure Output (when applicable)**

```txt
[generic/path/to/output/files]
└── [example-file.ts]
```

**Context Output Extension (when applicable)**

In addition to the mandatory links for generated or modified artifacts, the Context Output MUST report:

- [job-specific result, decision, count, limitation, or next action].

**Mandatory Context Output example**

The mandatory artifact links MUST be grouped under the producing job's logical identifier.

```md
- **validate-api-schemas**:
  - [user.schema.ts](apps/api/src/schemas/user.schema.ts)
  - [API Validation Report](.graph-engineering/runs/api/validate-api-schemas/OUTPUT-20260811-1030.md)
```

Example:

```md
- **Summary**: Validated 12 API schemas; 10 passed and 2 require review.
- **Limitation**: The payment-provider schema could not be validated because its source file is unavailable.
- **Next action**: Provide the payment-provider schema to complete validation.
```

Context Output MUST NOT be persisted or used as a downstream-job handoff.

On successful completion, the agent MUST report:

- [changes, findings, or handoff values].

On failure, the agent MUST report [error context, failing input, missing dependency, or target path].

## Prompt examples

```txt
[concise user prompt triggering this job]
```

```txt
[secondary prompt demonstrating contextual execution or parameters]
```
