# Read Actions Index

## Objective

The job MUST dump the contents of the centralized actions index file into the agent's context.

## Inputs

The job MUST NOT receive any inputs.

## Process

1. The agent MUST read and dump `apps/storefront/apis/actions.index.ts` into context.

## Output

The job MUST NOT produce any output files.

On successful completion, the agent MUST confirm that the file contents have been loaded into context.

## Prompt examples

```txt
Execute the read-actions-index job.
```
