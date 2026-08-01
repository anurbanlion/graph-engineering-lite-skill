# Jobs

A job is a bounded unit of work that can be executed independently or composed inside a graph.

A job defines the inputs it accepts, the process it follows, and the output it owns. It SHOULD focus on one responsibility so that it can be reused without depending on unrelated jobs.

## Location

Each job lives in:

```txt
graph-engineering/jobs/<job-name>/JOB.md
```

The directory name MUST use kebab case. `JOB.md` contains the human-readable contract for the job.

A reusable starting point is available in [`docs/job-template.md`](./job-template.md).

## Inputs

Inputs are the information available when the job begins.

They MAY come directly from the user, from the output of a previous job, from explicitly supplied files, or from project exploration when discovery is part of the job.

A job MUST distinguish the information the user provides from the information the agent is expected to discover or infer.

Example:

```txt
Journey: cart
Use cases:
- load-cart
- add-cart-item
```

In this example, the user selects the journey and use cases. The job may still discover service operations, DTOs, backend capabilities, existing implementations, and adaptation requirements.

## Process

The process describes how the job transforms its inputs into its output.

A simple job MAY use a short ordered sequence. A job involving exploration, planning, implementation, or validation SHOULD divide the process into named stages.

The process SHOULD describe meaningful operations, decisions, and boundaries. It SHOULD NOT attempt to document the agent's internal reasoning.

## Output

The output is the result owned by the job. Jobs commonly produce project outputs, managed outputs, or both.

### Project output

A project output creates or modifies repository files, such as source code, configuration, tests, or generated project structure.

The job MUST identify the expected result and the project paths it may affect.

### Managed output

A managed output is a persisted artifact produced by a run, commonly a Markdown document.

The persisted Markdown is the canonical record of that run. Because a graph may need the artifact content in its active context, a job with a managed Markdown output SHOULD support two additional execution modes.

#### Emit mode

Emit mode executes the job normally, persists the new Markdown artifact, and also places the complete generated content in the graph or conversation context.

This allows the next job to consume the result without locating and opening the artifact. The contextual content MUST represent the persisted artifact and SHOULD NOT be replaced by a summary.

#### Latest mode

Latest mode does not execute the job's analysis, generation, or transformation process. It locates the latest successful managed output for the same job and relevant domain, then places its complete Markdown content in the graph or conversation context.

Latest mode MUST NOT create a new managed output. If no matching output exists, the operation MUST fail clearly.

These modes describe graph behavior, not a required command-line interface. A graph MAY express them as job instructions. An implementation MAY provide flags, a job-specific script, or a shared output utility.

The managed output does not need to be converted into JSON solely for composition. Markdown MAY remain the exchange format when it is the canonical representation and can be consumed directly by the next agent or job.

Alternative names considered for these concepts include `context`, `publish`, or `forward` for Emit mode, and `replay`, `restore`, or `previous` for Latest mode. `Emit` and `Latest` describe the intended graph behavior without coupling it to standard streams or a specific implementation.

## Script

A job MAY use a script when part of its process benefits from deterministic behavior, such as locating files, validating inputs, transforming content, writing outputs, or retrieving a previous managed output.

Scripts are implementation details. The job concept and its graph behavior MUST remain understandable without requiring knowledge of how a script implements them.
