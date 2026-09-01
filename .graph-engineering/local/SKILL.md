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

1. The agent MUST start the job execution runtime when the user explicitly requests execution of a named job. For every explicit request to run a specific job, the agent MUST initialize the execution runtime as follows:


```bash
python3 .codex/skills/graph-engineering/scripts/execute.py --job execute-job --project-root <absolute-project-root>
```
Rules:

- The agent MUST use `python` if the `python3` binary is unavailable. When `python3` cannot be invoked, the agent MUST run the command with `python` instead.
- The agent MUST pass `execute-job` as the value of `--job` when starting a runtime. For this runtime-initialization command, `--job` MUST remain `execute-job`.
- The agent MUST replace `<absolute-project-root>` with the current project root’s absolute path. The command MUST contain the fully resolved path of the active project root in place of `<absolute-project-root>`.
- The agent MAY append `--execution-mode <mode>` ONLY if the user explicitly requests a special mode: `echo`, `latest`, or `iterative`. If not requested, the agent MUST omit the flag to use the default mode.
- The agent MAY append `--execution-mode <mode>` ONLY when the user explicitly requests `echo`, `latest`, or `iterative`. Without an explicit request for one of `echo`, `latest`, or `iterative` modes, the agent MUST omit `--execution-mode`.
- The runtime WILL return an `execution_id` that the agent MUST use to continue the execution. After starting the runtime, the agent MUST retain and reuse the returned `execution_id` for every continuation.

Example with a requested mode:
```bash
python3 .codex/skills/graph-engineering/scripts/execute.py --job execute-job --project-root <absolute-project-root>  --execution-mode echo
```

2. The agent MUST execute the `instructions` returned by the current runtime state. Every `instructions` returned by the current runtime state MUST be carried out by the agent.

Rules:

- The agent MUST NOT display intermediate runtime JSON payloads to the user. The agent MUST keep every intermediate runtime JSON payload hidden from the user.
- The agent MUST execute only the current state's `instructions` during this step. The agent MUST NOT execute an event's `instructions` until it selects that event.

3. The agent MUST select the single event whose `condition` matches the observed result. After completing the current state's `instructions`, the agent MUST choose exactly one event whose `condition` matches that result.

Rules:

- If the selected event contains `instructions`, the agent MUST execute that event's `instructions` BEFORE advancing the runtime. Before the runtime advances, the agent MUST complete every instruction defined by the selected event.

4. Advance the runtime by executing:

```bash
python3 .codex/skills/graph-engineering/scripts/execute.py <execution-id> <event>
```

- The first argument MUST be the exact `execution_id` returned by the first execution.
- The second argument MUST be the selected event.

4. The agent MUST advance the runtime with the selected event. The agent MUST use this command to continue the selected runtime execution:

```bash
python3 .codex/skills/graph-engineering/scripts/execute.py <execution-id> <event>
```

Rules:

- The agent MUST pass the exact `execution_id` returned when the runtime was first started as the first argument. The first command argument MUST be the original runtime `execution_id`.
- The agent MUST pass the selected event as the second argument. The second command argument MUST exactly match the event selected from the current state's `on` object.
- The agent MUST NOT terminate, summarize, or expose the result while a matching transition remains available. While any transition matches the observed result, the agent MUST continue the runtime instead of terminating or presenting a final result.

### Adding Context

The runtime maintains a `context` dictionary to track variables that can be used later by automated nodes. This `context` can be added or updated at any point on the runtime lifecycle.

Rules:

- When the selected transition's instructions require a context update, the agent MUST append `--context <key>=<value>` to the advance command. Every context update required by the selected transition MUST be passed through `--context` before the runtime advances.
- The agent MUST NOT append `--context` unless the selected transition's instructions explicitly require it. Without an explicit context-update instruction on the selected transition, the advance command MUST omit `--context`.
- The agent MAY append multiple `--context` flags when multiple updates are required. When the selected transition requires several context updates, the agent MAY pass each update through its own `--context` flag.

Example instruction with one context update:

```text
Add `my_key` with the value `my_value` to the runtime context.
```

The agent MUST interpret that instruction as:

```bash
python3 .codex/skills/graph-engineering/scripts/execute.py <execution-id> <event> --context my_key=my_value
```

Example instruction with a value resolved by the current process:

```text
Add the value resolved by this process as `my_key` to the runtime context.
```

The agent MUST interpret that instruction as:

```bash
python3 .codex/skills/graph-engineering/scripts/execute.py <execution-id> <event> --context my_key=<resolved-value>
```

- The agent MUST replace `<resolved-value>` with the actual value produced by the current process. The context update MUST contain the concrete resolved value instead of the placeholder.

Example instruction with multiple context updates:

```text
Add `my_key` with the value `my_value` and `another_key` with the value `another_value` to the runtime context.
```

The agent MUST interpret that instruction as:

```bash
python3 .codex/skills/graph-engineering/scripts/execute.py <execution-id> <event> --context my_key=my_value --context another_key=another_value
```

- The agent MUST append `--context job_name=<job-identifier>` when the user explicitly names a job identifier in kebab-case while starting a runtime. If the initial request already identifies the job, the runtime MUST receive that identifier as `job_name` from its first execution.

Example instruction with an initial job name:

```text
Execute the job `design-job`.
```

The agent MUST interpret that instruction as:

```bash
python3 .codex/skills/graph-engineering/scripts/execute.py --job execute-job --project-root <absolute-project-root> --context job_name=design-job
```

## Executing Scripts

- When a normal job process or a runtime state clearly instructs the agent to execute a specifically identified script, the agent MUST invoke that script through `execute_script`.

- When the agent invokes `execute_script`, it MUST do it as follows:

```bash
python3 .codex/skills/graph-engineering/scripts/execute_script.py <script-identifier> --project-root /absolute/path/to/project [-- <script-arguments>...]
```

- The agent MUST replace `<script-identifier>` with a snake_case identifier without `.py` or path separators.
- The agent MUST replace `/absolute/path/to/project` with the absolute Project Root.
- The agent MUST append all arguments for the resolved script only after `--`.

Example instruction without script arguments:

```text
Execute the script `list_jobs`.
```

The agent MUST interpret that instruction as:

```bash
python3 .codex/skills/graph-engineering/scripts/execute_script.py list_jobs --project-root /absolute/path/to/project
```

Example instruction with script arguments:

```text
Execute the script `resolve_local_job_path`.
Use these script arguments: `--project-root /absolute/path/to/project --job-identifier design-job`.
```

The agent MUST interpret that instruction as:

```bash
python3 .codex/skills/graph-engineering/scripts/execute_script.py resolve_local_job_path --project-root /absolute/path/to/project -- --project-root /absolute/path/to/project --job-identifier design-job
```

- The agent MUST NOT read, inspect, modify, or debug a skill script unless the user explicitly requests it.
- A script issue includes a non-zero exit code, a runtime error, an unavailable command, or an unexpected result that conflicts with the requested operation.
- When a script issue occurs, the agent MUST report the command, current working directory, and relevant output.
- The agent MUST NOT diagnose the issue automatically. The agent MUST ask the user whether they want the issue diagnosed before reading or inspecting any script.
