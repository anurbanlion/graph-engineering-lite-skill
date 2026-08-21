---
name: graph-engineering
description: Executes named jobs and graphs. Use when the user says to execute or list a job or graph, including requests such as "execute the compile-application-journeys job" or "run the application-design graph."
---

# Graph Engineering

- The agent MUST select and execute the appropriate job or graph according to an explicit user request.

- The agent MUST NOT execute or create a job or graph unless the user explicitly requests it.

## Writing style

The agent MUST use RFC-style normative language when creating a new job, graphs instructions or general writing style.

## Directory structure

```text
{local-skill-folder}/graph-engineering/
├── SKILL.md
├── templates/
│   └── job-template.md
├── graphs/
│   └── <graph-name>/
│       └── GRAPH.json
├── jobs/
│   └── <job-name>/
│       ├── JOB.md
│       └── GRAPH.md
└── scripts/
    ├── lib/
    └── custom/
```

* Each job and graph MUST be stored in its own directory.
* Each job definition MAY have a `JOB.md` file.
* Each job definition MAY have a `GRAPH.json` file.
* Each graph definition MUST be stored in a `GRAPH.json` file.
* Jobs and graphs MAY be organized in group directories at any depth.
* A job or graph logical identifier is the final directory name containing its definition file.
* Logical identifiers MUST be unique within their respective job or graph stores.

```text
{project-skill-folder}/
├── logs/
│   └── executions.log
└── runs/
    └── <domain>/
        └── <job-name>/
            └── <output-file>
```

## Executing jobs

1. When the user explicitly requests execution of a named job, the agent MUST start the job execution runtime from the project root by executing this exact command:

```bash
python3 .codex/skills/graph-engineering/scripts/execute.py
```

- The runtime MUST return an `execution_id` that the agent MUST use to continue this execution.

2. The agent MUST execute the `instructions` returned by the current runtime state.
3. The agent MUST NOT display intermediate runtime JSON payloads to the user.
4. After completing the current state's instructions, MUST select the single transition whose condition matches the observed result, and advance the runtime by executing:

```bash
python3 .codex/skills/graph-engineering/scripts/execute.py <execution-id> <event>
```
- The first argument MUST be the exact `execution_id` returned by the first execution, and the second argument MUST be the selected event.
- The agent MUST NOT terminate, summarize, or expose the result while a matching transition remains available.

## Executing Scripts

- The agent MUST NOT read, inspect, modify, or debug a skill script unless the user explicitly requests it.
- A script issue includes:
  - A technical failure, such as a non-zero exit code, runtime error, or unavailable command.
  - An unexpected result that conflicts with the requested operation or expected skill behavior, even when the script exits successfully.
- When a script issue occurs, the agent MUST report the command, current working directory, and relevant output.
- The agent MUST NOT diagnose the issue automatically. The agent MUST ask the user whether they want the issue diagnosed before reading or inspecting any script.
