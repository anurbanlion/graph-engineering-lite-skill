# Jobs

A job is a bounded unit of work that can be executed independently or composed inside a graph.

A job MUST define:

- which inputs it accepts
- the ordered process it follows
- the output it produces

A job SHOULD describe one responsibility. It MUST NOT duplicate the internal workflow of another job or depend on knowledge of unrelated jobs.

## Location

Each job MUST reside in:

```txt
graph-engineering/jobs/<job-name>/JOB.md
```

The directory name MUST be a kebab-case identifier. The document title SHOULD be the human-readable form of that identifier.

A job MAY use a script when deterministic file discovery, transformation, output writing, or validation is required.

## Inputs

Inputs are the information available when the job begins.

They MAY come directly from the user, from the output of a previous job, from explicitly supplied files (code, briefs, images, etc.), or from project exploration when discovery is part of the job.

Additionally, when producing a managed input, a job MUST specify a target domain to locate or place the artifact.

## Process

The process MUST describe how the job transforms its inputs into its output.

A simple job MAY use a short ordered sequence. A job involving exploration, planning, implementation, or validation SHOULD divide the process into ordered named stages.

The process SHOULD describe meaningful operations, decisions, and boundaries. It SHOULD NOT attempt to document the agent's internal reasoning.

## Output

The output is the result owned by the job. Jobs commonly produce project outputs, managed outputs, or both.

- Project output: A project output creates or modifies repository files, such as source code, configuration, tests, or generated project structure.
- Managed output: A managed output is a persisted artifact produced by a run, which takes the form of a Markdown document.

### Execution modes

Because a graph MAY require the artifact content in its active context or a job must build its output from a previous iteration, a job with a managed output SHOULD support additional execution modes:

- Managed output - Echo mode: Executes the job normally, persists the new Markdown artifact, but also places the complete generated content in the conversation context. This allows the next job to consume the result without locating and opening the artifact. The contextual content MUST represent the persisted artifact and SHOULD NOT be replaced by a summary.

- Managed output - Latest mode: Does not execute the job. It locates the latest successful managed output for the same job and relevant domain, then places its complete Markdown content in the graph or conversation context. Latest mode MUST NOT create a new managed output. If no matching output exists, the operation MUST fail clearly.

- Managed output - Iterative mode: Especial execution mode where it runs the job twice, once in latest mode and once y defaul mode, or echo if the user indicates so.

These execution modes complement the default managed output mode, which MUST only persist the output artifact and present a file link to the user. A graph MAY express these execution modes as job instructions.

## Script

A job MAY use a script when part of its process benefits from deterministic behavior, such as locating files, validating inputs, transforming content, writing outputs, or retrieving a previous managed output. A job process MAY consist entirely of just executing a script.