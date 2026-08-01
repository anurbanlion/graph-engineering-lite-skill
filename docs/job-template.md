# Job Template

Copy this template into:

```txt
graph-engineering/jobs/<job-name>/JOB.md
```

Remove sections that do not apply. Replace all bracketed placeholders.

```md
# [Job Title]

## Objective

The job MUST [describe the single owned outcome].

The job MUST NOT [state the most important scope exclusion, when needed].

## Inputs

The job MUST receive:

- [required input];
- [required input].

The job MAY receive:

- [optional constraint or context].

The agent MUST [discover or infer a value] when [condition].

Example:

```txt
[minimum valid user input or previous-job output]
```

## Required files

The following files MUST already exist:

```txt
[path/to/required-file]
[path/to/another-file]
```

When a required file is missing, the job MUST fail and report its path.

## Scope

The agent MAY inspect:

```txt
[allowed/path]
[allowed/path]
```

The agent MAY modify:

```txt
[allowed/output/path]
```

The agent MUST NOT modify the following unless the user explicitly requests it:

```txt
[protected/path]
[protected/path]
```

## Process

### 1. [First stage]

The agent MUST [observable responsibility].

The agent MUST NOT [constraint].

### 2. [Exploration or planning stage]

The agent MUST inspect [relevant context] to determine:

- [decision or fact];
- [decision or fact].

Before editing, the agent MUST produce a concise plan containing:

```txt
[plan field]: [example value]
[plan field]: [example value]
```

### 3. [Implementation or transformation stage]

The agent MUST [perform the bounded work].

The agent MUST preserve [existing behavior or unrelated content].

### 4. Validate

The agent MUST verify:

- [required outcome];
- [compatibility or formatting rule];
- [test or validation rule].

## Output

The job produces [project code / a managed Markdown artifact / structured standard output].

The canonical result is:

```txt
[output path or format]
```

On success, the agent MUST report:

- [completed unit];
- [changes or findings];
- [validation result].

On failure, the agent MUST report [affected input, file, domain, or dependency].

## Script

The agent MUST execute:

```bash
node scripts/custom/[script-name].mjs [arguments]
```

The agent MUST NOT reproduce the script's deterministic workflow manually.

### Output modes

Use this subsection only when the job has both a managed output and an executable script.

Default mode MUST execute the job and write a new managed artifact.

`--stdout` MUST execute the job, write the artifact, and print the complete generated content to standard output.

`--replay` MUST skip generation, locate the latest successful output for the same job and domain, and print it to standard output.

`--stdout` and `--replay` MUST be mutually exclusive.

When no replayable output exists, the script MUST report the error through standard error and exit non-zero.

## Examples

[Add a representative file structure, command, table, output, or implementation example.]

```txt
[example]
```

# Prompt examples

```txt
[concise prompt that selects this job]
```

```txt
[second representative prompt]
```
```

## Section checklist

Before accepting a new job, verify that:

- the objective owns one bounded outcome;
- user inputs and agent-discovered values are distinct;
- the minimum valid input has an example;
- required files are explicit;
- inspection, modification, and protected paths are explicit when relevant;
- the process is ordered and testable;
- output ownership and format are explicit;
- success and failure behavior are explicit;
- scripts and output modes are documented only when applicable; and
- prompt examples do not add hidden requirements.
