# List Pending Communications

## Objective

The job MUST list open communication tasks from initiatives.

The job MUST NOT draft communications or modify follow-up records.

## Inputs

The job MAY receive:

- one or more initiative domains in kebab-case.

## Process

1. When no initiative domain is supplied, the agent MUST execute `{skill}/scripts/custom/scan-open-communication-tasks.mjs` without arguments.
2. When one or more initiative domains are supplied, the agent MUST execute `{skill}/scripts/custom/scan-open-communication-tasks.mjs` with those domains as arguments.
3. The agent MUST use `global-tasks` as the managed-output domain when zero or multiple initiative domains are supplied; otherwise, it MUST use the supplied initiative domain.
4. The agent MUST resolve the managed-output path and write the matching initiative, owner, and task purpose.

## Output

The job MUST produce a Managed Output containing the pending tasks.

Output generation and formatting are executed manually by the agent.

```md
# Pending Tasks

## <initiative domain>

- (<owner>): <task purpose>
```

The managed output MUST NOT reproduce the `Communication` task marker or source-task checkbox.

On successful completion, the agent MUST report the output file link and task count.

On failure, the agent MUST report the scan or output-generation error.

## Prompt examples

```txt
Execute list-pending-communications job.
```

```txt
List pending communications for new-web-guidelines landing-financial-education.
```
