# Reflect on Job Execution

## Objective

The job MUST analyze the conversation history, user feedback, and the final outputs produced during the graph execution to derive a structured changelist for improving the job definitions that contributed to the identified gaps.

The job MUST autonomously identify which jobs in the executed graph are responsible for each gap; it MUST NOT rely on an external list of target jobs.

The job MUST NOT apply changes directly. It MUST produce a managed output artifact that a subsequent agent or the user can use to update the target jobs.

## Inputs

The job MUST NOT receive explicit inputs.

The job MUST have available in context:

- The conversation history from the current graph execution;
- The final project outputs (files, artifacts) paths produced during the execution.

## Process

**1. Gather Evidence**

1. The agent MUST review the conversation history to identify user corrections, preferences, recurring feedback, and explicit requests for process changes.
2. The agent MUST inspect the final project outputs to identify gaps between what the jobs prescribed and what was actually produced or corrected by the user.

**2. Trace Gaps to Source Jobs**

1. For each identified gap or user correction, the agent MUST determine which job in the executed graph is responsible — that is, which job's process or output template failed to account for the issue.
2. The agent MUST read the JOB.md definition of each identified job using `node scripts/read-jobs.mjs <job-name>`.
2.1. After reading each JOB.md, the agent MUST identify the exact existing step or output-template section for every recommendation. It MUST label the recommendation `Add`, `Modify`, or `Remove`. If no existing target exists, it MUST label it `Add new step` or `Add new section`.
3. The agent MUST compare each job's process and output template against the actual artifacts and behavior observed during execution.
4. The agent MUST flag any step that was skipped, reinterpreted, or manually corrected by the user during execution.
5. The agent MUST flag any output section that was consistently ignored, restructured, or deemed insufficient by the user.

**3. Produce Changelist**

1. For each affected job and each changed section, the agent MUST produce one complete `diff` block containing all proposed changes to that section. The agent MUST follow each block with a table containing `Change`, `Supporting Example`, and `Rationale` rows for the diff hunks; every `Change` value MUST begin with `Add`, `Modify`, or `Remove`.
2. Code MAY appear only in `Supporting Example` and only when the changed process concerns implementation. Code MUST NOT replace the process description in the diff.
3. Every change MUST be generalized. The agent MUST NOT propose journey-specific or instance-specific fixes. When the user corrected a concrete omission (e.g. a missing use case), the agent MUST trace the omission back to the process gap or classification criteria that caused it and propose a change that prevents the entire class of miss, not just the individual instance.
4. The changelist MUST be ordered by target job, then by section.

## Output

The job MUST produce a Managed Output as a Markdown document.

````md
# Execution Reflection Changelist

## Changes for `<job-identifier>`

### Process Changes

```diff
## Process

- existing step text
+ replacement or new step text
```

| Change | Supporting Example | Rationale |
| --- | --- | --- |
| Add: inventory screen sections before classification. | `HomeScreen` has Hero, Promotions, Featured Products, and Footer sections. | Footer was incorrectly dropped from the initial design. |
| Modify: classify route navigation as local unless it crosses an application boundary. | `setPersonalInfo(data)` is a local provider action, not a server action. | Local draft updates were incorrectly promoted to server actions. |

### Output Template Changes

```diff
## Output

- existing template text
+ replacement or new template text
```

| Change | Supporting Example | Rationale |
| --- | --- | --- |
| Add: `Detected Sections` table before `Use Cases`, organized by page. | `Home` \| `Promotions` \| `PromotionsSection` \| `packages/ui/src/.../PromotionsSection.tsx` | Preserves the screen's section architecture. |

## Changes for `<another-job-identifier>`

### Process Changes

```diff
## Process

- existing step text
+ replacement or new step text
```

| Change | Supporting Example | Rationale |
| --- | --- | --- |
````

On successful completion, the agent MUST report the jobs identified for improvement, the number of changes per job and section, and the managed output file link.

## Prompt examples

```txt
Execute the reflect-on-job-execution job.
```
