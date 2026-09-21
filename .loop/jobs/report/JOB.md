# Report

## Description

Produce a concise report of an assigned task or Job execution for the Orchestrator.

## Input

- The assigned task and Jobs;
- The tasks completed, artifacts changed, command and tool-call history, and relevant verification results.

## Process

1. List each completed task and its outcome.
2. List each created, modified, or relevant artifact with a link.
3. Record every search, console command, and internal tool call used, with its purpose and outcome.
4. Record verification results, unresolved issues, and required follow-up, then save the report as a Markdown artifact.

## Output

A Markdown report using this template:

```md
# Report - <task>

## Completed Tasks

- <task>: <outcome>

## Artifacts

- [<artifact>](<link>): <change or relevance>

## Commands and Tool Calls

| Type | Command or tool | Purpose | Outcome |
| --- | --- | --- | --- |
| Search | `<command or query>` | <purpose> | <outcome> |
| Console | `<command>` | <purpose> | <outcome> |
| Internal tool | `<tool call>` | <purpose> | <outcome> |

## Verification

- <verification and result>

## Unresolved Issues

- <issue or `None`>
```

The agent MUST return the link to this report to the Orchestrator.
