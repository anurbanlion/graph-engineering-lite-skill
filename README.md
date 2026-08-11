# Graph Engineering (Lite)

Graph Engineering (Lite) is a skill for running reusable work through **jobs** and **graphs**. From a user's perspective, you do not operate the internal scripts directly. You ask the agent to execute a job or graph, and the skill handles discovery, selection, validation, execution, outputs, and logging.

## Core concepts

### Job

A **job** is a reusable unit of work with a specific purpose, such as analyzing use cases, generating documentation, or implementing part of an application. Each job defines the instructions the agent must follow and, when applicable, the output it must produce.

Use a job when the request can be completed as one self-contained workflow.

Example requests:

- "Run the job that analyzes journey use cases."
- "Execute the API documentation job for this project."

### Graph

A **graph** connects multiple jobs into a larger workflow. It defines which job runs first and what should happen after each job succeeds or fails.

Use a graph when the request requires several coordinated steps rather than one isolated task.

Example requests:

- "Run the graph that builds the application use cases."
- "Execute the application design graph."

### Run

A **run** is one execution of a job within a project. When a job produces an artifact, the skill stores it under the project's `.graph-engineering/runs` directory. Runs are grouped by domain and job name so outputs remain organized and traceable.

```text
<project-folder>/
└── .graph-engineering/
    ├── logs/
    │   └── executions.log
    └── runs/
        └── <domain>/
            └── <job-name>/
                └── <output-file>
```

The **project folder** is the user's working project. `.graph-engineering` is the skill-managed directory created inside that project for execution data.

### Output types

Jobs MAY create **Project Outputs** in the repository, **Managed Outputs** as persisted Markdown artifacts under `.graph-engineering/runs`, or both. Every successfully completed job also produces a **Context Output**: a non-persisted message for the user that links every file created or modified during that execution. Context Output is user-facing only.

## How it works

1. You explicitly ask the agent to run a job or graph.
2. The skill discovers the available options and selects the one that best matches your request.
3. For a job, the skill reads and executes that job's instructions.
4. For a graph, the skill validates the workflow and begins with its initial job.
5. The skill follows the graph's success or failure transitions until it completes or aborts.
6. Generated outputs are written to the appropriate run directory, and execution activity is logged.

The skill does not create or execute jobs or graphs without an explicit request.

## Features

- **Reusable jobs:** define focused workflows once and run them across projects.
- **Composable graphs:** combine jobs into multi-step processes with success and failure paths.
- **Automatic discovery:** selects from the jobs or graphs available in the skill.
- **Graph validation:** checks workflow references before execution begins.
- **Managed outputs:** stores generated artifacts in deterministic project locations.
- **Context outputs:** always reports links to files generated or modified in the current execution.
- **Execution logs:** records activity under `.graph-engineering/logs`.
- **Safe execution:** requires explicit user intent and stops invalid graphs before downstream work runs.
- **Resumable interaction:** a graph may pause for missing user input and continue from the same job once that input is provided.

## Using the skill

Ask the agent for the outcome you want and mention a job or graph when you already know its name. You do not need to invoke the internal scripts yourself.

```text
Run the analyze-journey-use-cases job for the checkout flow.
```

```text
Execute the build-application-use-cases graph for this project.
```

When you do not know the available names, ask the agent to show the jobs or graphs first.

```text
What jobs are available in Graph Engineering Lite?
```

```text
Show me the available graphs and explain what each one does.
```

## Repository structure

The repository contains the skill definition, reusable job definitions, graph definitions, internal scripts used by the agent, and a root-level synchronization pipeline.

```text
graph-engineering-lite-skill/
├── README.md
├── graph-engineering/
│   ├── SKILL.md
│   ├── jobs/
│   │   └── <job-name>/
│   │       └── JOB.md
│   ├── graphs/
│   │   └── <graph-name>/
│   │       └── GRAPH.json
│   └── scripts/
├── .env
└── bin/
    ├── sync-folder.mjs
    ├── sync-folder.sh
    └── sync-folder.bat
```

The scripts inside `graph-engineering` support discovery, reading, validation, output-path resolution, and logging. Normal users interact with the skill through natural-language requests to the agent.

## Folder synchronization pipeline

The synchronization pipeline copies the local `graph-engineering` folder into a configured Codex skills directory. It is intended for maintaining the skill in this repository and publishing the latest local version into another project without manually deleting and copying folders.

The pipeline consists of:

- `bin/sync-folder.mjs`: reads configuration, validates paths, replaces each destination, creates directories, and copies recursively.
- `bin/sync-folder.sh`: macOS/Linux wrapper.
- `bin/sync-folder.bat`: Windows wrapper.

### Configuration

Copy `.env.example` to `.env` in the repository root and configure the paths:

```env
SYNC_SOURCE_PATH=graph-engineering
SYNC_DESTINATION_PATH=["C:\\path\\to\\project-a\\.codex\\skills\\graph-engineering","C:\\path\\to\\project-b\\.codex\\skills\\graph-engineering"]
```

`SYNC_SOURCE_PATH` may be relative to the repository root or absolute. `SYNC_DESTINATION_PATH` accepts either one absolute path or a JSON array of absolute paths. Each path identifies the exact folder that will be replaced by the source folder; destination paths must be distinct and must not contain one another.

All failures are printed to standard error and return a non-zero exit code.

### How to use the sync

1. Ensure the wrapper is executable:

```sh
chmod +x bin/sync-folder.sh
```

2. Review `.env` file for correct paths. 

3. Run the wrapper for your platform:

```sh
./bin/sync-folder.sh
```

```bat
bin\sync-folder.bat
```

Each destination folder is replaced completely on each successful run. Changes already present only in a destination folder are therefore deleted.

# TODO

- Add support for job groups
- Add support for graph groups
- Create a rename job node
