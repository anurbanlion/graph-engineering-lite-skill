# Jobs

A job is a bounded unit of work that can run independently or as part of a graph.

It describes what information is needed, what work is performed, and what result is produced. A job should focus on one responsibility so it can be reused and composed without depending on unrelated jobs.

## Location

Each job lives in:

```txt
graph-engineering/jobs/<job-name>/JOB.md
```

The directory name uses kebab case. The `JOB.md` file contains the human-readable contract for that job.

A reusable starting point is available in [`docs/job-template.md`](./job-template.md).

## Inputs

Inputs are the information available when the job begins.

They may come directly from the user, from the result of a previous job, from explicitly supplied files, or from project exploration when discovery is part of the job.

A job should make clear which information the user must provide and which information the agent is expected to determine.

Example:

```txt
Journey: cart
Use cases:
- load-cart
- add-cart-item
```

Here, the user selects the journey and use cases. The job may still need to discover service operations, DTOs, backend capabilities, and implementation details.

## Process

The process explains how the job transforms its inputs into its output.

Simple jobs may use a short ordered sequence. Jobs involving exploration, planning, implementation, or validation are easier to understand when the process is divided into named stages.

The process should describe meaningful steps and boundaries rather than internal reasoning details.

## Output

An output is the result owned by the job. There are two common forms.

### Project output

The job creates or modifies project files.

Examples include source code, configuration, tests, or generated project structure. The affected paths and expected result should be clear in the job definition.

### Managed output

The job writes a persisted artifact, commonly a Markdown document stored with the run outputs.

For jobs that generate a managed output through a script, three execution forms are useful:

- Default execution generates and stores a new output.
- `--stdout` generates and stores a new output, then prints the same content to standard output.
- `--replay` skips generation, finds the latest output for the same job and domain, and prints it to standard output.

`--stdout` is useful when another job or an agent needs the newly generated content without opening the file. `--replay` is useful when the latest persisted result should be reused without repeating the work.

The managed file remains the persisted result. Its content may stay in Markdown when that is the natural format; it does not need to be converted into JSON solely for job composition.

## Script

A job may use a script when part of the work should be deterministic, such as locating files, validating inputs, transforming content, writing outputs, or replaying a previous result.

The `JOB.md` explains when and how the script is used. The script contains the deterministic implementation details.
