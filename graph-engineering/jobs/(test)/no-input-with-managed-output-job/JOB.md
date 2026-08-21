# No-Input Managed Output Job

## Objective

The job MUST generate a Managed Output Markdown document whose complete content is `test`.

The job MUST NOT require user input, inspect repository files, or create Project Output.

## Inputs

The job MUST NOT require input.

## Process

1. The agent MUST create the resolved Markdown file with `test` as its complete content.

## Output

The job MUST produce one Managed Output at:

The output generation and serialization MUST be executed manually by the agent.

**Markdown Document Output**

```md
test
```

## Prompt examples

```txt
Execute the no-input-with-managed-output-job job.
```

```txt
Run (test)/no-input-with-managed-output-job.
```
