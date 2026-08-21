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
job-graph-engineering/
├── SKILL.md
├── templates/
│   └── job-template.md
├── graphs/
│   └── <graph-name>/
│       └── GRAPH.json
├── jobs/
│   └── <job-name>/
│       └── JOB.md
└── scripts/
    ├── resolve-output-path.mjs
    ├── dump-latest-output.mjs
    ├── list-graphs.mjs
    ├── read-graphs.mjs
    ├── validate-graph.mjs
    ├── lib/
    │   ├── activity-logs.mjs
    │   └── resolve-paths.mjs
    └── custom/
```

* Each job and graph MUST be stored in its own directory.
* Each job definition MUST be stored in a `JOB.md` file.
* Each graph definition MUST be stored in a `GRAPH.json` file.
* Jobs and graphs MAY be organized in group directories at any depth.
* A job or graph logical identifier is the final directory name containing its definition file.
* Logical identifiers MUST be unique within their respective job or graph stores.

```text
.{local-skill-folder}/
├── logs/
│   └── executions.log
└── runs/
    └── <domain>/
        └── <job-name>/
            └── <output-file>
```

* .`{local-skill-folder}` is resolved by the internal skill scripts and is located on the project folder the skill is being used.

## Job output types

A job MAY produce a Project Output, a Managed Output, or both. Every successfully completed job MUST produce a Context Output:

- **Project Output**: Creates or modifies repository files directly (such as source code, configuration files, tests, or generated directory structures).
- **Managed Output**: Creates a persisted Markdown document artifact produced by a run, stored at `.{local-skill-folder}/runs/<domain>/<job-name>/OUTPUT-timestamp.md`.
- **Context Output**: A non-persisted message directed to the user. It MUST list links to every Project Output created or modified and every Managed Output generated during the current job execution, grouped by the producing job's logical identifier. When the job generates or modifies no file artifacts, it MUST explicitly state that no file artifacts were generated. A job MAY define additional Context Output requirements in its `JOB.md`. Those requirements MUST extend the mandatory artifact-link list; they MUST NOT replace it. Local links in Context Output MUST use normalized absolute paths with `/` as the separator, for example `[Artifact](C:/Users/.../artifact.md)`. Markdown link destinations MUST NOT use `\` separators.

## Executing jobs

1. When the user explicitly requests execution of a named job, the agent MUST start the job execution runtime from the project root by executing:

```bash
python3 .codex/skills/graph-engineering/scripts/execute.py
```

- The runtime MUST return an `execution_id` that the agent MUST use to continue this execution.

2. The agent MUST NOT display intermediate runtime JSON payloads to the user.
3. The agent MUST execute the `instructions` returned by the current runtime state.
4. After completing the current state's instructions, MUST select the single transition whose condition matches the observed result, and advance the runtime by executing:

```bash
python3 .codex/skills/graph-engineering/scripts/execute.py <execution-id> <event>
```
- The first argument MUST be the exact `execution_id` returned by the first execution, and the second argument MUST be the selected event.
- The agent MUST NOT terminate, summarize, or expose the result while a matching transition remains available.

## Executing Scripts

- The agent MUST execute skill scripts from the project root using their project-relative location under `<local-skill-folder>/graph-engineering/scripts/`

Example:

```bash
node .codex/skills/graph-engineering/scripts/validate-graph.mjs.
```

- The agent MUST NOT read, inspect, modify, or debug a skill script unless the user explicitly requests it.
- A script issue includes:
  - A technical failure, such as a non-zero exit code, runtime error, or unavailable command.
  - An unexpected result that conflicts with the requested operation or expected skill behavior, even when the script exits successfully.
- When a script issue occurs, the agent MUST report the command, current working directory, and relevant output.
- The agent MUST NOT diagnose the issue automatically. The agent MUST ask the user whether they want the issue diagnosed before reading or inspecting any script.

### Usage examples


```bash
# Resolve managed output path for a job and domain
$ node scripts/resolve-output-path.mjs global-designs compile-storefront-journeys
/home/user/projects/my-project/.local-skill-folder/runs/global-designs/compile-storefront-journeys/OUTPUT-20260801-1053.md
```

```bash
# Dump latest managed output content into context
$ node scripts/dump-latest-output.mjs global-designs compile-storefront-journeys
===== LATEST MANAGED OUTPUT: global-designs / compile-storefront-journeys (OUTPUT-20260801-1053.md) =====
# Application Journeys

- account
- checkout
- storefront
===== END LATEST MANAGED OUTPUT =====
```

```bash
# List available graphs
$ node scripts/list-graphs.mjs
build-application-use-cases
build-journey-architecture
```

```bash
# Read a single graph definition
$ node scripts/read-graphs.mjs build-application-use-cases
===== GRAPH: build-application-use-cases =====
{
  "name": "build-application-use-cases",
  "version": "1.0",
  "initial": "analyze-journey-use-cases",
  "jobs": {
    "analyze-journey-use-cases": {
      "instructions": [
        "Use <route-journey>-page as the run/<domain> name."
      ],
      "onDone": "compile-storefront-use-cases",
      "onError": "abort"
    },
    "compile-storefront-use-cases": {
      "instructions": [
        "Use global-designs as the run/<domain> name."
      ],
      "onDone": "complete",
      "onError": "abort"
    }
  }
}
===== END GRAPH: build-application-use-cases =====
```

```bash
# Read multiple graph definitions
$ node scripts/read-graphs.mjs build-application-use-cases build-journey-architecture
===== GRAPH: build-application-use-cases =====
{
  "name": "build-application-use-cases",
  "version": "1.0",
  ...
}
===== END GRAPH: build-application-use-cases =====
===== GRAPH: build-journey-architecture =====
{
  "name": "build-journey-architecture",
  "version": "1.0",
  ...
}
===== END GRAPH: build-journey-architecture =====
```

```bash
# Validate a valid graph definition (version must match the graph's declared version)
$ node scripts/validate-graph.mjs 2.0 build-application-use-cases
Graph is valid: build-application-use-cases
Version: 2.0
Definition: /home/user/projects/my-project/graph-engineering/graphs/build-application-use-cases/GRAPH.json
```

```bash
# Validate an invalid graph definition
$ node scripts/validate-graph.mjs 2.0 invalid-graph
Graph validation failed: invalid-graph
- "initial" MUST be a non-empty string.
```
