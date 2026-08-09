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
3. The agent MUST compare each job's process and output template against the actual artifacts and behavior observed during execution.
4. The agent MUST flag any step that was skipped, reinterpreted, or manually corrected by the user during execution.
5. The agent MUST flag any output section that was consistently ignored, restructured, or deemed insufficient by the user.

**3. Produce Changelist**

1. For each identified misalignment, the agent MUST produce a change entry specifying:
   - **Target**: The logical identifier of the affected job.
   - **Section**: `Process` or `Output Template`.
   - **Current behavior**: What the job currently prescribes.
   - **Proposed behavior**: What the job SHOULD prescribe to align with the user's vision.
   - **Rationale**: Why this change is recommended, referencing specific conversation evidence or output gaps.
2. Every change MUST be generalized. The agent MUST NOT propose journey-specific or instance-specific fixes. When the user corrected a concrete omission (e.g. a missing use case), the agent MUST trace the omission back to the process gap or classification criteria that caused it and propose a change that prevents the entire class of miss, not just the individual instance.
3. The changelist MUST be ordered by target job, then by section.

## Output

The job MUST produce a Managed Output as a Markdown document.

```md
# Execution Reflection Changelist

## Changes for `<job-identifier>`

### Process Changes

| # | Current Behavior | Proposed Behavior | Rationale |
| --- | --- | --- | --- |
| 1 | The agent classifies hooks under relevant use cases. | The agent MUST also document which hook state maps to which use case parameter. | User repeatedly asked for hook-to-parameter traceability during execution. |

### Output Template Changes

| # | Current Behavior | Proposed Behavior | Rationale |
| --- | --- | --- | --- |
| 1 | Models table includes `Fields` and `Notes` columns. | Add a `Source Hint` column indicating the suspected backend origin. | The audit repeatedly discovered sources that could have been anticipated at design time. |

## Changes for `<another-job-identifier>`

### Process Changes

| # | Current Behavior | Proposed Behavior | Rationale |
| --- | --- | --- | --- |

### Output Template Changes

| # | Current Behavior | Proposed Behavior | Rationale |
| --- | --- | --- | --- |
```

On successful completion, the agent MUST report the jobs identified for improvement, the number of changes per job and section, and the managed output file link.

## Prompt examples

```txt
Execute the reflect-on-job-execution job.
```
