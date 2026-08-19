# Do Tasks

## Objective

The job MUST execute a selected task from a domain task list, respecting the task's execution constraints (`USER`, `USER_AUTHORIZATION`, `USER_REVIEW`) and templates (`Templates`), and MUST update the task status in-place within the task list file upon completion.

## Inputs

The job MUST receive:

- `domain`: initiative domain name;
- `task file path`: project-relative path to the Markdown task list file.

The job MAY receive:

- `task file content`: the Markdown task list content dump provided in context;
- `target task`: title or description of the specific task to execute.

Examples:

```txt
domain: gtd-tool
task file path: .graph-engineering/runs/gtd-tool/add-tasks/OUTPUT-20260819-0601.md
```

```txt
domain: chikiarena
task file path: .graph-engineering/runs/chikiarena/add-tasks/OUTPUT-20260815-1200.md
target task: Clarify Chiquiarena direction
```

## Scope

The agent MAY inspect:

```txt
[task file path]
.graph-engineering/runs/
```

The agent MAY modify:

```txt
[task file path]
```

## Process

**1. Read Task File Content**

1. If `task file content` is not provided in context, the agent MUST read `task file path` using native file viewing tools (`view_file`) to obtain the current task list content.

**2. Resolve Target Task**

1. If `target task` is provided in the input or context, the agent MUST attempt to match it against the pending tasks `[ ]` in `task file content`.
2. If `target task` is not provided or is not found among the pending tasks `[ ]` in `task file content`, the agent MUST present the list of pending tasks `[ ]` to the user and ask the user to select which task to execute.

**3. Evaluate Execution Constraints**

1. The agent MUST inspect the selected task for execution constraint clause comments (`<!-- USER -->`, `<!-- USER AUTHORIZATION -->`, `<!-- USER REVIEW -->`).
2. The agent MUST enforce the rules specified by each clause:
   - `USER`: The agent MUST halt automatic execution, present the required action to the user, and wait for the user to perform it.
   - `USER_AUTHORIZATION`: The agent MUST request explicit user authorization before executing the task actions or state-changing operations.
   - `USER_REVIEW`: The agent MUST pause execution after completing the task action and ask the user to review the work accomplished up to that point. When both `USER_AUTHORIZATION` and `USER_REVIEW` are present on a task, the agent MUST request authorization before starting the task, execute the work upon approval, and then pause for user review upon completion.

Example task execution constraints:

```md
- [ ] <!-- USER --> Review production deployment logs <!-- context: conversation; estimate: 10m -->
- [ ] <!-- USER_AUTHORIZATION --> Run database migration script <!-- context: job; job: db-migrate; estimate: 10m -->
- [ ] <!-- USER_REVIEW --> Verify UI responsive layout <!-- context: conversation; estimate: 10m -->
- [ ] <!-- USER_AUTHORIZATION --> <!-- USER_REVIEW --> Refactor payment gateway module <!-- context: conversation; estimate: 30m -->
```

**4. Evaluate Templates**

1. The agent MUST first identify whether the selected task corresponds to a reusable template defined under `## Templates`.
2. If the selected task corresponds to a template, the agent MUST transition directly to **Execute Task - Template mode**.

**5. Execute Task**

1. If the selected task does NOT correspond to a template, the agent MUST perform the work specified by the task according to its context environment (`conversation`, `job`, `skill`) while strictly adhering to the evaluated execution constraints.
2. The agent MUST track observations, issues, or findings during execution.

Example standard task completion:

> Before execution (`task file path`)
```md
- [ ] Create initial initiatives <!-- estimate: 60m; added-at: 1786931520 -->
  - [ ] Create the GTD tool initiative <!-- context: job; job: create-initiatives; estimate: 10m; added-at: 1786931520 -->
  - [ ] Create the YouTube initiative <!-- context: job; job: create-initiatives; estimate: 10m; added-at: 1786931520 -->
```

> After executing `Create the GTD tool initiative`
```md
- [ ] Create initial initiatives <!-- estimate: 60m; added-at: 1786931520 -->
  - [x] Create the GTD tool initiative <!-- context: job; job: create-initiatives; estimate: 10m; added-at: 1786931520; done-at: 1787064430 -->
  - [ ] Create the YouTube initiative <!-- context: job; job: create-initiatives; estimate: 10m; added-at: 1786931520 -->
```

**6. Execute Task - Template mode**

1. If the selected task corresponds to a template, the agent MUST execute this stage instead of the standard **Execute Task** stage.
2. The agent MUST iterate through each template child step in order:
   - Evaluate the child step's execution constraints (`<!-- USER -->`, `<!-- USER_AUTHORIZATION -->`, `<!-- USER_REVIEW -->`).
   - Perform the work for agent-executable steps.
3. The agent MUST materialize (copy) the executed child steps as `[x]` with `done-at` timestamp into the task list under the parent task.
4. The agent MUST materialize (copy) any subsequent `<!-- USER -->` steps as pending `[ ]` (unmarked) into the task list under the parent task, continuing until reaching a step not marked with `<!-- USER -->`.

Example template task materialization and completion:

> Before execution (`task file path`)
```md
- [ ] Create the do-tasks job <!-- estimate: 60m; added-at: 1787064430 -->
```

> Template in `## Templates`
```md
- [ ] Create the X job <!-- estimate: 60m -->
  - [ ] MUST execute `design-job` job to produce the initial Managed Output <!-- context: job; job: design-job; estimate: 10m -->
  - [ ] <!-- USER --> Review the X job template's inputs <!-- context: conversation; estimate: 10m -->
  - [ ] <!-- USER --> Review the X job template's process <!-- context: conversation; estimate: 10m -->
  - [ ] Commit updated job design to git <!-- context: conversation; estimate: 5m -->
  - [ ] <!-- USER --> Review the X job template overall <!-- context: conversation; estimate: 10m -->
```

> After executing `MUST execute design-job...`
```md
- [ ] Create the do-tasks job <!-- estimate: 60m; added-at: 1787064430 -->
  - [x] MUST execute `design-job` job to produce the initial Managed Output <!-- context: job; job: design-job; estimate: 10m; added-at: 1787064430; done-at: 1787064430 -->
  - [ ] <!-- USER --> Review the do-tasks job template's inputs <!-- context: conversation; estimate: 10m; added-at: 1787064430 -->
  - [ ] <!-- USER --> Review the do-tasks job template's process <!-- context: conversation; estimate: 10m; added-at: 1787064430 -->
```

**6.1 Template Modification Mid-Execution**

1. If the template definition under `## Templates` is modified or updated during task execution, the agent MUST re-evaluate and re-materialize the template steps from the beginning according to the updated template structure, unless explicitly instructed otherwise by the user.

Example template modification mid-execution:

> Initial template in `## Templates`
```md
- [ ] Template X
  - [ ] Task 1 <!-- context: conversation; estimate: 10m -->
  - [ ] Task 2 <!-- context: conversation; estimate: 10m -->
  - [ ] <!-- USER --> Task 3 <!-- context: conversation; estimate: 10m -->
```

> Initial materialization in task list after executing Task 1
```md
- [ ] Parent Task
  - [x] Task 1 <!-- context: conversation; estimate: 10m; added-at: 1787064430; done-at: 1787064430 -->
  - [ ] Task 2 <!-- context: conversation; estimate: 10m; added-at: 1787064430 -->
  - [ ] <!-- USER --> Task 3 <!-- context: conversation; estimate: 10m; added-at: 1787064430 -->
```

> Completely updated template in `## Templates` mid-execution
```md
- [ ] Template X
  - [ ] New Task 1 <!-- context: conversation; estimate: 10m -->
  - [ ] New Task 2 <!-- context: conversation; estimate: 10m -->
  - [ ] <!-- USER --> New Task 3 <!-- context: conversation; estimate: 10m -->
```

> Re-materialization in task list reflecting new template (preserving completed work)
```md
- [ ] Parent Task
  - [x] Task 1 <!-- context: conversation; estimate: 10m; added-at: 1787064430; done-at: 1787064430 -->
  - [ ] New Task 1 <!-- context: conversation; estimate: 10m; added-at: 1787064450 -->
  - [ ] New Task 2 <!-- context: conversation; estimate: 10m; added-at: 1787064450 -->
  - [ ] <!-- USER --> New Task 3 <!-- context: conversation; estimate: 10m; added-at: 1787064450 -->
```

**6.2 Tasks Outside Template**

1. If custom child tasks that are not part of the template definition under `## Templates` are manually inserted under a parent task, the agent MUST execute these non-template child steps sequentially when encountered, mark them completed as `[x]` with `done-at: <UNIX timestamp>`, and then resume normal template execution.

Example tasks outside template:

> Template in `## Templates`
```md
- [ ] Template X
  - [ ] Template Task 1 <!-- context: conversation; estimate: 10m -->
  - [ ] Template Task 2 <!-- context: conversation; estimate: 10m -->
  - [ ] <!-- USER --> Template Task 3 <!-- context: conversation; estimate: 10m -->
```

> Task list with custom inserted task (`Custom Task A`) outside template
```md
- [ ] Parent Task 1
  - [x] Template Task 1 <!-- context: conversation; estimate: 10m; added-at: 1787064430; done-at: 1787064430 -->
  - [ ] Custom Task A <!-- context: conversation; estimate: 10m; added-at: 1787064440 -->
```

> Task list after executing Custom Task A
```md
- [ ] Parent Task 1
  - [x] Template Task 1 <!-- context: conversation; estimate: 10m; added-at: 1787064430; done-at: 1787064430 -->
  - [x] Custom Task A <!-- context: conversation; estimate: 10m; added-at: 1787064440; done-at: 1787064450 -->
  - [ ] Template Task 2 <!-- context: conversation; estimate: 10m; added-at: 1787064430 -->
  - [ ] <!-- USER --> Template Task 3 <!-- context: conversation; estimate: 10m; added-at: 1787064430 -->
```

**7. Mark Task Done In-Place**

1. The agent MUST edit `task file path` directly, changing `[ ]` to `[x]` for the completed task.
2. The agent MUST append `done-at: <UNIX timestamp>` to the completed task line without altering unrelated tasks or sections.

- The agent MUST NOT write a separate Managed Output artifact; all task state updates MUST be written directly to `task file path`.

## Output

The job MUST modify `task file path` in-place by marking the completed task as `[x]` with `done-at: <UNIX timestamp>`.

Output generation, serialization, and formatting are executed manually by the agent.

**Context Output Extension**

In addition to the mandatory links for modified artifacts, the Context Output MUST report:

On successful completion:
- Executed task title and completion timestamp (`done-at`);
- File link to `task file path`;
- Summary of work accomplished or user actions requested;
- Next suggested pending task in `task file path`.

On failure:
- Reason for failure (e.g. missing input parameters, unresolvable target task, or execution errors).

## Prompt examples

```txt
Execute do-tasks job for domain `gtd-tool` using task file `.graph-engineering/runs/gtd-tool/add-tasks/OUTPUT-20260819-0601.md`.
```

```txt
Execute the `do-tasks` job in two sequential steps:
1. Load its definition into context by running `design-job` in Latest mode with domain `do-tasks`.
2. Immediately proceed to execute `do-tasks` in Default mode using the loaded process.

Inputs for `do-tasks` job:
- domain: gtd-tool
- task file path: .graph-engineering/runs/gtd-tool/add-tasks/OUTPUT-20260819-0601.md
```
