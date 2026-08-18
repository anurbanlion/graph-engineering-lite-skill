# Add Tasks

## Objective

The job MUST transform free-form initiative ideas into an agent-centered Markdown task list with actionable tasks, optional one-level subtasks, execution-context metadata, human-only markers when needed, duration estimates, and task-added timestamps.

The job MUST help an agent understand what can be advanced next, where each task should be executed, what user input is needed, how large each task is, and when each task was added.

The job MUST NOT execute tasks, create database rows, create calendar blocks, send communications, or modify repository project files.

## Inputs

The job MUST receive:

- a kebab-case domain identifier for exactly one initiative;
- source context with task ideas, needs, decisions, goals, or free-form notes.

The job MAY receive:

- an existing task list for the same initiative.

Examples:

```txt
Execute add-tasks job in iterative mode:

domain: chikiarena
context: Hay que ordenar que se necesita hacer para avanzar Chikiarena: revisar estado actual, definir oferta, validar siguientes pasos.
```

```txt
Execute add-tasks job in iterative mode:

domain: chikiarena
context: revisar si ya existe logo, decidir si la landing va primero, e investigar referencias de estructura web.
```

## Process

**1. Validate Input**

1. The agent MUST confirm that the domain is kebab-case and represents one initiative.
2. The agent MUST request source context when no task ideas, needs, decisions, goals, or notes are provided.
3. The agent MUST use existing tasks when they are provided or loaded on context.

**2. Task Formulation and Ownership**

1. The agent MUST convert explicit work into concrete tasks.
2. The agent MUST prefer agent-centered task formulations that let the agent ask, prepare, propose, execute, inspect, or request feedback instead of assigning broad work to the human.
3. When user involvement is needed, the agent MUST first try to formulate the task as an agent action that requests the needed input, decision, authorization, private access, or feedback from the user.
4. The agent MUST preserve relevant existing tasks and avoid duplicates.
5. The agent MUST use parent tasks only to group two or more direct subtasks.
6. The agent MUST NOT create nesting deeper than one parent and one child level.
7. The agent MUST NOT mark agent-operable tasks with a responsibility field; agent execution MUST be the default when no `human-only: true` marker is present.
8. The agent MUST mark a leaf task with `human-only: true` only when the user is the only party who can complete the task because it requires a private decision, private access, payment, offline action, subjective approval, or personal feedback that cannot be delegated.
9. The agent SHOULD split mixed human-agent work into agent-operable coordination tasks and narrow `human-only: true` tasks instead of using shared ownership labels.
10. The agent MUST use the `Clarify tasks for: <target>` prefix for top-level actions that do not have child tasks unless they have a template associated. The `<target>` MUST be an actionable task title that begins with a verb.

Example:

```md
- [ ] Clarify tasks for: Define payment flow <!-- context: conversation; estimate: 10m; added-at: <UNIX timestamp> -->
```

**3. Estimates and Timestamps**

1. The agent MUST estimate each leaf task in minutes.
2. The agent MUST split any leaf task estimated above 10 minutes into smaller leaf tasks.
3. The agent MUST set each parent estimate to the sum of its child estimates; parent tasks MAY exceed 10 minutes.
4. The agent MUST add an `added-at` UNIX timestamp (seconds since epoch) to every newly added task using the current job execution timestamp.
5. The agent MUST preserve existing `added-at` timestamps during iterative merges.
6. When preserving an existing task that lacks `added-at`, the agent MUST add the current job execution UNIX timestamp.

**4. Context Metadata**

1. The agent MUST add `context: conversation` to tasks that are executed in the active conversation through interviewing, asking, proposing, validating, collecting input, or requesting feedback.
2. The agent MUST add `context: job` to tasks that require reading, executing, improving, or otherwise using a job; when the exact job is known, the agent SHOULD also add `job: <job-name>` with the logical job identifier.
3. The agent MAY use `context: skill` for tasks that require a skill rather than a job; when the exact skill is known, the agent SHOULD also add `skill: <skill-name>`.
4. The agent MUST use another clear `context: <context-name>` value when a task is neither conversation-based, job-based, nor skill-based, and the task title or metadata MUST make the execution setting unambiguous.

**5. References**

1. The agent MUST classify reusable user-provided task behavior as one of: `References`, `Templates`, or `Processing Local Rules`.
2. The agent MUST place factual context, boundaries, and reusable source notes in `References`.

Example:

```md
## References

- The legacy Pages Router implementation remains the source of section order.
```

**6. Templates**

1. The agent MUST place reusable task shapes in `Templates`.
2. A template MUST include the literal Markdown task shape that agents MUST materialize, including its title, context metadata, estimates, and any child steps.
3. The agent MUST place constraints for applying a specific template directly below that template without changing its task steps.
4. The agent MUST keep conditional execution guidance outside the template unless the user explicitly makes it a template step.
5. When recording a completed template child, the agent MUST preserve the template child's title and metadata exactly; it MAY only change `[ ]` to `[x]` and add `done-at`.
6. When materializing a child task from a parent/template after completion, the agent MUST inherit the parent/template `added-at` timestamp and record the actual completion time separately as `done-at`.
7. The agent MUST ensure every template parent estimate equals the sum of its template child estimates; rules and conditional guidance that are not template steps MUST NOT affect that sum.

Example:

```md
## Templates

- Agents MUST use the following template when creating or executing a task named `analyze-components`:

  - [ ] Analyze components <!-- context: conversation; estimate: 20m -->
    - [ ] Extract every component and add it as a task <!-- context: conversation; estimate: 10m -->
    - [ ] Review existing component tasks <!-- context: conversation; estimate: 10m -->
  - Rules:
    - Skip a component when an equivalent task already exists.
```

**7. Processing Local Rules**

1. The agent MUST place task-list custom transformation behavior in `Processing Local Rules`.
2. The agent MUST preserve user-defined task processing rules when creating generated tasks.
3. The agent MUST treat user feedback about how task ideas should be transformed as a `Processing Local Rule`.

Example:

```md
## Processing Local Rules

- Insert generated migration tasks before analysis tasks while retaining prior migration tasks above them.
```

Example transformation:

```txt
Input: Necesitamos revisar el estado actual de Chiquiarena, decidir la oferta y ver si una landing deberia ir primero.
```

```md
- [ ] Clarify Chiquiarena direction <!-- context: conversation; estimate: 50m; added-at: 1771190400 -->
  - [ ] Locate current Chiquiarena notes <!-- context: conversation; estimate: 10m; added-at: 1771190400 -->
  - [ ] Summarize current Chiquiarena status <!-- context: conversation; estimate: 10m; added-at: 1771190400 -->
  - [ ] Propose possible first offers <!-- context: conversation; estimate: 10m; added-at: 1771190400 -->
  - [ ] Ask user to choose the first Chiquiarena offer <!-- context: conversation; estimate: 10m; added-at: 1771190400 -->
  - [ ] Request user decision on whether landing page goes first <!-- context: conversation; estimate: 10m; added-at: 1771190400; human-only: true -->
```

Example iterative merge:

> Previous tasks
```md
- [ ] Clarify Chiquiarena direction <!-- context: conversation; estimate: 40m; added-at: 1771190400 -->
  - [ ] Locate current Chiquiarena notes <!-- context: conversation; estimate: 10m; added-at: 1771190400 -->
  - [ ] Summarize current Chiquiarena status <!-- context: conversation; estimate: 10m; added-at: 1771190400 -->
  - [ ] Propose possible first offers <!-- context: conversation; estimate: 10m; added-at: 1771190400 -->
  - [ ] Ask user to choose the first Chiquiarena offer <!-- context: conversation; estimate: 10m; added-at: 1771190400 -->
```

> Input
```txt
Agrega revisar si ya existe logo e investigar referencias de estructura web.
```

> Transformation
```md
- [ ] Clarify Chiquiarena direction <!-- context: conversation; estimate: 40m; added-at: 1771190400 -->
  - [ ] Locate current Chiquiarena notes <!-- context: conversation; estimate: 10m; added-at: 1771190400 -->
  - [ ] Summarize current Chiquiarena status <!-- context: conversation; estimate: 10m; added-at: 1771190400 -->
  - [ ] Propose possible first offers <!-- context: conversation; estimate: 10m; added-at: 1771190400 -->
  - [ ] Ask user to choose the first Chiquiarena offer <!-- context: conversation; estimate: 10m; added-at: 1771190400 -->
- [ ] Prepare Chiquiarena web direction <!-- context: conversation; estimate: 30m; added-at: 1771276800 -->
  - [ ] Check whether a Chiquiarena logo already exists <!-- context: conversation; estimate: 10m; added-at: 1771276800 -->
  - [ ] Collect three reference web structures <!-- context: conversation; estimate: 10m; added-at: 1771276800 -->
  - [ ] Summarize reference structure patterns <!-- context: conversation; estimate: 10m; added-at: 1771276800 -->
```

Example agent-centered reformulation with job and conversation contexts:

> Input
```txt
Realizar la primera prueba de ejecucion del nuevo servicio y validar la calidad del resultado.
```

> Transformation
```md
- [ ] Prepare and evaluate service trial run <!-- context: conversation; estimate: 30m; added-at: 1771276800 -->
  - [ ] Ask user for parameters needed for service trial run <!-- context: conversation; estimate: 10m; added-at: 1771276800 -->
  - [ ] Execute service trial run with provided parameters <!-- context: job; estimate: 10m; added-at: 1771276800 -->
  - [ ] Review trial execution output and give qualitative feedback <!-- context: conversation; estimate: 10m; added-at: 1771276800; human-only: true -->
```

## Output

The job MUST produce a Managed Output: one Markdown task artifact for the initiative domain.

Output generation and formatting are executed manually by the agent.

Output format:

```md
- [ ] <task title> <!-- context: conversation | job | skill | <context-name>; estimate: <minutes>m; added-at: <UNIX timestamp> -->
  - [ ] <conversation child task title> <!-- context: conversation; estimate: <minutes>m; added-at: <UNIX timestamp> -->
  - [ ] <known-job child task title> <!-- context: job; job: <job-name>; estimate: <minutes>m; added-at: <UNIX timestamp> -->
  - [ ] <unknown-job child task title> <!-- context: job; estimate: <minutes>m; added-at: <UNIX timestamp> -->
  - [ ] <known-skill child task title> <!-- context: skill; skill: <skill-name>; estimate: <minutes>m; added-at: <UNIX timestamp> -->
  - [ ] <human-only child task title> <!-- context: conversation | job | skill | <context-name>; estimate: <minutes>m; added-at: <UNIX timestamp>; human-only: true -->

## References

- <additional information, caveat, source note, or idea fragment related to the tasks>

## Templates

- Agents MUST use the following template when creating or executing a task named `<template-task-name>`:

```md
- [ ] <literal template task> <!-- context: <context-name>; estimate: <minutes>m -->
  - [ ] <literal template child step> <!-- context: <context-name>; estimate: <minutes>m -->
```

- Rules:
  - <constraint for applying this template without changing its task steps>

## Processing Local Rules

- <rule for transforming or ordering the initiative task list>

## Transformation pointers

- <transformation pointer derived from user feedback or source context>
```

On successful completion, the agent MUST report:

- the initiative domain;
- the managed-output file link;
- the number of parent tasks and leaf tasks added;

On failure, the agent MUST report the missing or invalid domain, missing context, unavailable existing task list, or output-generation error.

## Prompt examples

```txt
Execute add-tasks job in iterative mode, if there is no latest, continue with default execution:

domain: chikiarena
context: Hay que ordenar que se necesita hacer para avanzar Chikiarena: revisar estado actual, definir oferta, validar siguientes pasos.
```

```txt
Execute add-tasks job in iterative mode:

domain: chikiarena
context: revisar si ya existe logo, decidir si la landing va primero, e investigar referencias de structure web.
```
