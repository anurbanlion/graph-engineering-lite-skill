# Instruction Authoring Guide

## Writing Sequential Instructions

Instruction lists MUST describe actions in the order the agent performs them. Each primary instruction MUST begin with `The agent` and MUST use RFC 2119 language such as MUST, MUST NOT, SHOULD, or MAY.

Critical instructions SHOULD repeat the same requirement in a second, paraphrased sentence. The repetition MUST preserve the same meaning and MUST NOT introduce a new action.

## Adding Rules

Each primary instruction MAY include a `Rules:` block immediately after it. Rules MUST add constraints, required values, prohibitions, or argument requirements for that primary instruction. Rules MUST NOT introduce a new sequential action that belongs in a later primary instruction.

## Template

```md
1. The agent MUST perform <primary action>. The agent MUST complete <primary action> before continuing.

Rules:

- The agent MUST use <required value>.
- The agent MUST NOT use <forbidden value>.
```

## Example

```md
1. The agent MUST start the job execution runtime when the user explicitly requests a named job. For every explicit request to run a specific job, the agent MUST initialize the execution runtime.

Rules:

- The agent MUST pass `execute-job` as the value of `--job`. For this runtime-initialization command, `--job` MUST remain `execute-job`.
- The agent MUST replace `<absolute-project-root>` with the current project root's absolute path. The command MUST contain the fully resolved active project root.

2. The agent MUST execute the current runtime state's `instructions`. Every instruction returned by the current runtime state MUST be carried out by the agent.

Rules:

- The agent MUST NOT display intermediate runtime JSON payloads to the user. The agent MUST keep every intermediate runtime JSON payload hidden from the user.
```
