# Add Tasks

## Objective

The job MUST transform free-form initiative ideas into a Markdown task list with actionable tasks, optional one-level subtasks, execution responsibility, and duration estimates.

The job MUST help a human and an agent understand what can be done next, who or what can do it, and how large each task is.

The job MUST NOT execute tasks, create database rows, create calendar blocks, send communications, or modify repository project files.

## Inputs

The job MUST receive:

- a kebab-case domain identifier for exactly one initiative;
- source context with task ideas, needs, decisions, goals, or free-form notes.

The job MAY receive:

- an existing task list for the same initiative.

Examples:

```txt
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

**2. Add or Update Tasks**

1. The agent MUST convert explicit work into concrete tasks.
2. The agent MUST preserve relevant existing tasks and avoid duplicates.
3. The agent MUST use parent tasks only to group two or more direct subtasks.
4. The agent MUST NOT create nesting deeper than one parent and one child level.
5. The agent MUST mark each task with `responsible: human` or `responsible: ai`.
6. The agent MUST use `responsible: human` only when the task requires a human decision, authorization, taste, payment, private access, or offline action.
7. The agent MUST use `responsible: ai` when an agent can do the task; this does not mean a human cannot do it.
8. The agent MUST estimate each leaf task in minutes.
9. The agent MUST split any leaf task estimated above 10 minutes into smaller leaf tasks.
10. The agent MUST set each parent estimate to the sum of its child estimates; parent tasks MAY exceed 10 minutes.

Example transformation:

```txt
Input: Necesitamos revisar el estado actual de Chiquiarena, decidir la oferta y ver si una landing deberia ir primero.
```

```md
- [ ] Clarify Chiquiarena direction <!-- responsible: human; estimate: 50m -->
  - [ ] Locate current Chiquiarena notes <!-- responsible: ai; estimate: 10m -->
  - [ ] Summarize current Chiquiarena status <!-- responsible: ai; estimate: 10m -->
  - [ ] List possible first offers <!-- responsible: ai; estimate: 10m -->
  - [ ] Choose the first Chiquiarena offer <!-- responsible: human; estimate: 10m -->
  - [ ] Choose whether the landing page goes first <!-- responsible: human; estimate: 10m -->
```

Example iterative merge:

> Previous tasks
```md
- [ ] Clarify Chiquiarena direction <!-- responsible: human; estimate: 40m -->
  - [ ] Locate current Chiquiarena notes <!-- responsible: ai; estimate: 10m -->
  - [ ] Summarize current Chiquiarena status <!-- responsible: ai; estimate: 10m -->
  - [ ] List possible first offers <!-- responsible: ai; estimate: 10m -->
  - [ ] Choose the first Chiquiarena offer <!-- responsible: human; estimate: 10m -->
```

> Input
```txt
Agrega revisar si ya existe logo e investigar referencias de estructura web.
```

> Transformation
```md
- [ ] Clarify Chiquiarena direction <!-- responsible: human; estimate: 40m -->
  - [ ] Locate current Chiquiarena notes <!-- responsible: ai; estimate: 10m -->
  - [ ] Summarize current Chiquiarena status <!-- responsible: ai; estimate: 10m -->
  - [ ] List possible first offers <!-- responsible: ai; estimate: 10m -->
  - [ ] Choose the first Chiquiarena offer <!-- responsible: human; estimate: 10m -->
- [ ] Prepare Chiquiarena web direction <!-- responsible: ai; estimate: 30m -->
  - [ ] Check whether a Chiquiarena logo already exists <!-- responsible: ai; estimate: 10m -->
  - [ ] Collect three reference web structures <!-- responsible: ai; estimate: 10m -->
  - [ ] Summarize reference structure patterns <!-- responsible: ai; estimate: 10m -->
```

**3. Write Output**

1. The agent MUST produce only the Markdown task list as the managed output.
2. The agent MUST omit analysis, recommendations, and explanatory sections from the managed output.

## Output

The job MUST produce a Managed Output: one Markdown task list for the initiative domain.

Output generation and formatting are executed manually by the agent.

Output format:

```md
- [ ] <task title> <!-- responsible: human | ai; estimate: <minutes>m -->
  - [ ] <child task title> <!-- responsible: human | ai; estimate: <minutes>m -->
```

On successful completion, the agent MUST report:

- the initiative domain;
- the managed-output file link;
- the number of parent tasks and leaf tasks added;

On failure, the agent MUST report the missing or invalid domain, missing context, unavailable existing task list, or output-generation error.

## Prompt examples

```txt
domain: chikiarena
context: Hay que ordenar que se necesita hacer para avanzar Chikiarena: revisar estado actual, definir oferta, validar siguientes pasos.
```

```txt
Execute add-tasks job in iterative mode:

domain: chikiarena
context: revisar si ya existe logo, decidir si la landing va primero, e investigar referencias de structure web.
```
