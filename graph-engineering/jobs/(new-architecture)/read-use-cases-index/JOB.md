# Read Use Cases Index

## Objective

The job MUST dump the contents of the centralized use cases index file into the agent's context.

## Inputs

The job MUST NOT receive any inputs.

## Process

1. The agent MUST read and dump `apps/storefront/apis/use-cases.index.ts` into context.

## Output

The job MUST NOT produce any output files.

On successful completion, the agent MUST confirm that the file contents have been loaded into context.

## Prompt examples

```txt
Execute the read-use-cases-index job.
```
