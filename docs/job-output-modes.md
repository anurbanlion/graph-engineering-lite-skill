# Job Output Modes

## Purpose

This document defines a common execution contract for jobs that:

- produce a managed output artifact; and
- use a script to generate that artifact.

The contract lets an agent consume job results through standard output instead of opening managed output files.

Jobs that do not generate a managed output artifact, or that do not have an executable script, are outside this contract.

## Output ownership

The managed artifact remains the canonical persisted result of the job.

The script MUST write the artifact before reporting success.

Standard output is a delivery mechanism for the same artifact content. It is not a second canonical representation and does not require converting Markdown into JSON.

## Execution modes

### Default mode

The script MUST execute the job process and write a new managed output artifact.

By default, the script MAY print a concise human-readable execution summary, but it MUST NOT print the complete artifact unless `--stdout` is provided.

Example:

```bash
node scripts/custom/analyze-journey-use-cases.mjs <output-path> [...inputs]
```

### Standard-output mode

The `--stdout` option MUST execute the normal job process, write the new managed output artifact, and then print the complete generated artifact to standard output.

The content printed to standard output MUST match the content written to the artifact.

The option MUST NOT prevent artifact creation.

Example:

```bash
node scripts/custom/analyze-journey-use-cases.mjs <output-path> [...inputs] --stdout
```

### Replay mode

The `--replay` option MUST skip the job analysis, generation, or transformation process.

It MUST locate the latest successful managed output produced by the same job for the selected domain and print its complete content to standard output.

Replay mode MUST NOT create, modify, rename, or copy an artifact.

If no previous successful output exists for that job and domain, the script MUST print an explanatory error to standard error and exit with a non-zero status code.

Example:

```bash
node scripts/custom/analyze-journey-use-cases.mjs --domain cart --replay
```

## Domain resolution

A replay-capable job MUST receive or resolve the domain used to locate previous outputs.

The script MUST search only outputs belonging to:

1. the same job; and
2. the selected domain.

It MUST select the most recent successful output according to the repository's managed-output naming or metadata convention.

The script MUST NOT replay an output from another job or infer a different domain.

## Option compatibility

`--stdout` and `--replay` MUST NOT be used together.

When both options are provided, the script MUST print an explanatory error to standard error and exit with a non-zero status code.

Replay mode already emits the complete persisted output to standard output.

## Standard streams

The complete artifact content MUST be printed only to standard output.

Errors and diagnostics MUST be printed to standard error.

When complete artifact content is emitted, the script SHOULD avoid mixing summaries, labels, paths, or logs into standard output. Execution metadata SHOULD be written to the normal activity log or standard error when needed.

## Examples

Generate and persist an analysis without emitting the complete Markdown:

```bash
node scripts/custom/analyze-journey-use-cases.mjs <output-path> --journey cart
```

Generate, persist, and emit the same Markdown:

```bash
node scripts/custom/analyze-journey-use-cases.mjs <output-path> --journey cart --stdout
```

Emit the latest persisted analysis without running analysis again:

```bash
node scripts/custom/analyze-journey-use-cases.mjs --domain cart --replay
```

The same contract can apply to a resolver job:

```bash
node scripts/custom/resolve-journey-service-context.mjs <output-path> --journey cart --stdout
node scripts/custom/resolve-journey-service-context.mjs --domain cart --replay
```

## Job documentation requirements

A job adopting this contract MUST document:

- whether the contract applies;
- how its domain is supplied or resolved;
- the default execution command;
- the `--stdout` command;
- the `--replay` command;
- how the latest successful output is selected; and
- its failure behavior when no replayable output exists.

## Scope

This document defines a reusable convention. It does not automatically change existing jobs or scripts.

Each applicable job MUST adopt and implement the contract explicitly.