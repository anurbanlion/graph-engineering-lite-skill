# Read Documentation

## Objective

The job MUST receive and read the available documentation paths.

## Inputs

The job MUST receive one or more documentation file paths.

## Process

1. The agent MUST verify that one or more documentation paths were supplied.
2. The agent MUST read only the supplied documentation paths.
4. The agent MUST report a missing or unreadable supplied file as an error.

## Output

The job MUST produce only Context Output.

For each supplied file read successfully, the Context Output MUST state that the file was read correctly and MUST include a link or file reference to it.

Example:

```md
- **read-documentation**:
  - Documentation read: [USAGE.md](/absolute/path/analytics/docs/USAGE.md)
```

On failure, the agent MUST report the missing or unreadable supplied file.

## Prompt examples

```txt
Execute the read-documentation job for these files:

- analytics/docs/USAGE.md
- analytics/docs/TRACKING.md
```
