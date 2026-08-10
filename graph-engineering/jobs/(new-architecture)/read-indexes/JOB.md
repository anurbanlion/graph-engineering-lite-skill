# Read Indexes

## Objective

The job MUST dump the contents of one or more index files into the agent's context.

The job MUST NOT classify operations, recommend reuse, or make architecture decisions. Reading is context preparation only.

## Inputs

The job MUST receive:

- One or more absolute or project-relative file paths to index files, provided via graph instructions.

## Process

1. For each supplied file path, the agent MUST read and dump the file contents into context.
2. The agent MUST NOT interpret, transform, or act on the file contents.

## Output

The job MUST NOT produce any output files.

On successful completion, the agent MUST confirm which files were loaded into context.

## Prompt examples

```txt
Execute the read-indexes job.
```
