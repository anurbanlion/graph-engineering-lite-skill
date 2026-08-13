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
    ├── read-job-template.mjs
    ├── read-jobs.mjs
    ├── list-jobs.mjs
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

**Job discovery**

1. The agent MUST execute `node scripts/list-jobs.mjs` before selecting a job.
2. The agent MUST use the returned relative paths to identify the single job that best matches the explicit user request.
3. The agent MUST use only the selected job's logical identifier when calling `read-jobs.mjs`.
4. The agent MUST NOT read any job definition before selecting its logical identifier.
5. The agent MUST read the selected job by executing `node scripts/read-jobs.mjs <job-name>`.

> Note: `read-jobs.mjs` MAY accept multiple job names, but the agent MUST NOT use that capability in the current workflow.

> Note: If no available job name reasonably matches the user request, the agent MUST halt execution and inform the user that no suitable job is available.

> Note: If two listed job paths share a logical identifier, the agent MUST halt execution and report the ambiguity.

**Job pre-execution**

6. If a job requires an input that is not available, the agent MUST pause the job execution, ask the user for the missing input, and resume the same job after receiving it.
7. If the selected job produces a managed output, the agent MUST resolve the output path by executing `node scripts/resolve-output-path.mjs <domain> <job-name>`. The agent MUST NOT create an alternative output path manually.
8. If executing in **Latest mode**, the agent MUST **NOT** execute the `JOB.md` process, create project files, or run job scripts (this affects execution regardless of whether the job produces a managed output, project output, or both).
9. If executing in **Latest mode** and the job produces a managed output, the agent MUST dump the latest output into context by executing `node scripts/dump-latest-output.mjs <domain> <job-name>`. If no output exists, the agent MUST report failure and halt unless the active graph job instructions explicitly define a fallback strategy, e.g. continue the next job.
10. If executing in **Iterative mode**, the agent MUST first execute the job in Latest mode and then execute it in Default mode. If the user explicitly requests Echo mode, the second execution MUST use Echo mode instead of Default mode. If execution of the first job fails because there is no a latest manage output, halt execution, inform the user and ask if the agent should continue with the second execution.

> Note: A managed-output domain name is a required input whenever `resolve-output-path.mjs` requires it. The agent MUST ask for it when absent and MUST NOT infer it.

**Job execution**

11. If the selected job produces project outputs, the agent MUST execute the job process according to its `JOB.md` instructions to create or modify repository files.
12. If the selected job produces a managed output, the agent MUST execute the job process according to its `JOB.md` instructions and write the output Markdown artifact to the path resolved in **Job pre-execution**.
13. Upon successful job completion, the agent MUST present a **Context Output** to the user. It MUST group every link under the producing job's logical identifier and link every Project Output created or modified and every Managed Output generated during the current job execution. It MUST NOT link merely available artifacts from earlier executions. If the job generated or modified no file artifacts, it MUST explicitly state that result. The job's `JOB.md` MAY require additional user-facing information in this Context Output. Example:

```md
- **design-journey-use-cases**:
  - [Journey Use-Case Design](.graph-engineering/runs/account/design-journey-use-cases/OUTPUT-20260811-1030.md)
  - [account.contract.ts](apps/storefront/apis/account/domain/contracts/account.contract.ts)
```

14. If executing in **Echo mode** and the job produces a managed output, the agent MUST dump the managed output into context by executing `node scripts/dump-latest-output.mjs <domain> <job-name>`.

## Executing graphs

**Graph discovery**

1. The agent MUST execute `node scripts/list-graphs.mjs` before selecting a graph.
2. The agent MUST use the returned relative paths to identify the single graph that best matches the explicit user request.
3. The agent MUST use only the selected graph's logical identifier when calling `read-graphs.mjs` or `validate-graph.mjs`.
4. The agent MUST NOT read any graph definition before selecting its logical identifier.
5. The agent MUST read the selected graph by executing `node scripts/read-graphs.mjs <graph-name>`.

> Note: `read-graphs.mjs` MAY accept multiple graph names, but the agent MUST NOT use that capability in the current workflow.

> Note: If no available graph name reasonably matches the user request, the agent MUST halt execution and inform the user that no suitable graph is available.

> Note: If two listed graph paths share a logical identifier, the agent MUST halt execution and report the ambiguity.

**Graph validation**

6. The agent MUST validate the selected graph by executing `node scripts/validate-graph.mjs <version> <graph-name>` before executing its first job. The `<version>` argument MUST match the `version` field declared in the graph's `GRAPH.json` definition.
7. If graph validation fails, the agent MUST stop the graph execution and inform the user of the validation errors.

**Graph execution**

7. The agent MUST begin execution with the job referenced by `initial`.
8. The agent MUST execute each job according to the `## Executing jobs` section and the additional `instructions` defined for that job in the graph.
9. If a job requires an input that is not available, the agent MUST pause the graph execution, ask the user for the missing input, and resume the same job after receiving it.
10. The agent MUST NOT inspect manually a managed output artifact (i.e. reading a file) to derive a downstream job input, a system for the managed output to be visible on context is already taken into account with managed output modes.
11. After a successful job execution, the agent MUST continue with the job or terminal outcome defined by `onDone`.
12. After a failed job execution, the agent MUST continue with the job or terminal outcome defined by `onError`.
13. Upon successful graph completion, the agent MUST present a consolidated **Context Output** containing file links grouped by producing job for every Project Output modified and Managed Output generated during that graph execution.

## Graph parsing rules

* `name` identifies the graph.
* `version` identifies the graph definition version.
* `example-prompts` MAY contain a non-empty array of non-empty example prompts that show users how to invoke the graph. These are example prompts and MUST NOT be followed unless they come from the user directly.
* `initial` identifies the first job to execute.
* `jobs` contains the jobs participating in the graph.
* Each key inside `jobs` MUST match an available job logical identifier.
* `instructions` provides additional execution context for a job.
* `onDone` defines the next job or terminal outcome after a successful execution.
* `onError` defines the next job or terminal outcome after a failed execution, a failed execution is a job missing or an error on a custom script.
* `complete` is a terminal outcome that means the graph finished successfully.
* `abort` is a terminal outcome that means the graph MUST stop. The agent MUST explain which job failed and why the graph was aborted.
* A missing required input is not automatically an error. The agent SHOULD ask the user for the missing input and resume execution.
* The graph runner MUST report an invalid graph when `initial`, `onDone`, or `onError` references an unknown job or terminal outcome.
* Inputs, user interaction, output resolution, and output writing remain controlled by each job and the skill workflow.
* Structured standard output is the preferred interface for passing machine-readable values between graph jobs.
* Managed output artifacts MUST NOT be treated as implicit downstream input interfaces.
* The graph MUST NOT duplicate the internal process, inputs, or output format already defined by a job.

## Executing Scripts

- The agent MUST execute skill scripts from the project root using project-relative paths.
- The agent MUST NOT read, inspect, modify, or debug a skill script unless the user explicitly requests it.
- A script issue includes:
  - A technical failure, such as a non-zero exit code, runtime error, or unavailable command.
  - An unexpected result that conflicts with the requested operation or expected skill behavior, even when the script exits successfully.
- When a script issue occurs, the agent MUST report the command, current working directory, and relevant output.
- The agent MUST NOT diagnose the issue automatically. The agent MUST ask the user whether they want the issue diagnosed before reading or inspecting any script.

### Usage examples

```bash
# List available jobs
$ node scripts/list-jobs.mjs
analyze-journey-use-cases
compile-storefront-journeys
compile-storefront-use-cases
create-job
scaffold-journey-architecture
```

```bash
# Read the canonical job template
$ node scripts/read-job-template.mjs
===== JOB TEMPLATE =====
# [Job Title]
...
===== END JOB TEMPLATE =====
```

```bash
# Read a single job definition
$ node scripts/read-jobs.mjs compile-storefront-use-cases
===== JOB: compile-storefront-use-cases =====
# Compile Storefront Use Cases

## Objective
...
===== END JOB: compile-storefront-use-cases =====
```

```bash
# Read multiple job definitions
$ node scripts/read-jobs.mjs compile-storefront-journeys compile-storefront-use-cases
===== JOB: compile-storefront-journeys =====
# Compile Storefront Journeys
...
===== END JOB: compile-storefront-journeys =====
===== JOB: compile-storefront-use-cases =====
# Compile Storefront Use Cases
...
===== END JOB: compile-storefront-use-cases =====
```

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
