# Jobs

A job is a bounded unit of work that can be executed independently or composed inside a graph.

A job defines:

- which inputs it accepts
- the ordered process it follows
- the output it produces

A job SHOULD describe one responsibility. It MUST NOT duplicate the internal workflow of another job or depend on knowledge of unrelated jobs.

## Location

Each job lives in:

```txt
graph-engineering/jobs/<job-name>/JOB.md
```

The directory name MUST be a kebab-case identifier. The document title SHOULD be the human-readable form of that identifier.

A job MAY use a script when deterministic file discovery, transformation, output writing, or validation is required.

## Sections

Every `JOB.md` SHOULD use the following sections.

### Objective

Defines the single outcome owned by the job.

The objective MUST describe the result, not a sequence of implementation steps.

### Inputs

Defines everything required to begin execution.

Inputs MAY come from:

- the user;
- structured standard output from a previous job;
- explicitly supplied files or source code; or
- project inspection when the job explicitly permits discovery.

The section SHOULD include a concrete example showing the minimum valid input.

The job MUST distinguish user-provided inputs from values the agent is expected to discover or infer.

### Required files

Lists files that MUST exist before execution when applicable.

The job MUST report missing required files rather than silently creating unrelated structure unless creation is part of its objective.

### Process

Defines the ordered stages of execution.

The process SHOULD be divided into named stages when the work includes exploration, planning, implementation, validation, or reporting.

Each stage MUST define observable responsibilities and constraints. It SHOULD avoid prescribing low-level reasoning that does not affect the result.

### Output

Defines the resulting project changes, managed artifact, standard output, or combination of these.

The section MUST state:

- the canonical result;
- the required format;
- whether an artifact is written;
- what is printed on success;
- what is printed on failure; and
- whether the result can be consumed by another job.

### Examples

Provides representative commands, prompts, structures, or file contents.

Examples MUST illustrate the contract without introducing requirements absent from the normative sections.

### Prompt examples

Shows concise user requests that should select the job.

## Scripts

A job SHOULD use a script when its operation benefits from deterministic behavior, including:

- locating files or managed outputs;
- parsing repeated command-line inputs;
- generating or transforming artifacts;
- creating predictable project structure;
- validating identifiers or paths; or
- emitting exact output contracts.

The agent MUST execute the script rather than reproduce its internal deterministic workflow manually.

Scripts MUST send errors to standard error and exit with a non-zero status code on failure.

## Managed outputs

A managed output is a persisted artifact produced by a job, commonly Markdown stored under the repository's run-output convention.

The persisted artifact is the canonical result. Standard output is a delivery channel that allows an agent or downstream job to consume the same content without opening the artifact manually.

Jobs that have both a managed output and an executable script SHOULD support the following modes.

### Default mode

Runs the job and writes a new managed output.

The script MAY print a concise summary, but it SHOULD NOT print the complete artifact unless requested.

### `--stdout`

Runs the normal job process, writes the managed output, and prints the complete generated content to standard output.

The emitted content MUST match the persisted artifact. Summaries, labels, paths, and diagnostics MUST NOT be mixed into standard output while the complete artifact is being emitted.

### `--replay`

Skips analysis, generation, and transformation. It locates the latest successful output for the same job and selected domain and prints the complete persisted content to standard output.

Replay mode MUST NOT create or modify artifacts. If no matching output exists, the script MUST report the error through standard error and exit non-zero.

`--stdout` and `--replay` MUST be mutually exclusive.

Markdown outputs do not need to be converted to JSON. A downstream language model may consume the emitted Markdown directly.

## Output composition

A graph MAY pass standard output from one job to another.

The producing job owns the output format. The consuming job MUST document which values or content it expects and MUST NOT rediscover them from a managed artifact when standard output already provides them.

Jobs SHOULD prefer stable, explicit output contracts. Structured JSON is appropriate when exact machine-readable fields are required. Markdown is appropriate when tables, narrative analysis, or mixed human-readable content are the canonical result.

## Failure behavior

A job MUST fail clearly when:

- required inputs are missing;
- required files do not exist;
- identifiers or paths are invalid;
- required project capabilities cannot be found;
- a requested operation exceeds the documented scope; or
- a replayable output does not exist.

Failure reports MUST identify the affected input, file, domain, use case, or dependency whenever possible.

## Writing rules

Job contracts MUST use RFC-style normative terms consistently:

- `MUST` and `MUST NOT` for requirements;
- `SHOULD` and `SHOULD NOT` for strong defaults; and
- `MAY` for permitted alternatives.

Requirements SHOULD be concise, testable, and located in the section where they apply.

A job MUST avoid references to unrelated jobs, graphs, or architecture unless that relationship is part of its explicit public contract.
