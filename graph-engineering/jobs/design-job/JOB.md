# Design Job

## Objective

The job MUST design a job definition through an iterative conversation and produce the designed job as a local Managed Output.

The job MUST NOT integrate the designed job into the main jobs repository.

The job MUST NOT treat repository migration as part of design validation.

## Inputs

The job MAY receive any combination of the following optional inputs, including none of them:

- A proposed job name;
- A proposed Managed Output domain;
- The job's objective;
- The job's expected inputs;
- The job's expected outputs;
- The job's process;
- The job's requirements;
- An existing draft or legacy job definition;
- Prior conversation or design notes;

Although execution rules mandates a domain as an input for jobs with a Managed Output, this case is an exception since the domain is derived during **4. Resolve Name**.

Examples:

```txt
Execute the design-job job to design a job that compiles initiatives from project notes.
```

```txt
Execute design-job job.
```

## Scope

The agent MAY inspect:

```txt
<skill-local-folder>/graph-engineering/templates/job-template.md
<skill-local-folder>/graph-engineering/jobs/**/JOB.md
```

The agent MAY modify:

```txt
.graph-engineering/runs/<domain>/design-job/OUTPUT-*.md
.graph-engineering/runs/<domain>/design-job/*.mjs
```

The agent MUST NOT modify the following:

```txt
<skill-local-folder>/graph-engineering/jobs/**/JOB.md
<skill-local-folder>/graph-engineering/graphs/**/GRAPH.json
```

## Process

- Rules, criteria, and notes around a process action SHOULD be written as bullets beneath that action instead of as separate numbered steps.
- The job process MUST NOT include standard graph-engineering execution operations as numbered steps, including collecting mandatory inputs, resolving the Managed Output path, writing the Managed Output, or presenting the required Context Output. The job process MAY describe one of these operations only when the designed job adds behavior beyond the standard execution rule, and that additional behavior MUST be stated explicitly.

**1. Receive Initial Context**

1. The agent MUST collect any provided job name, description, legacy definition, requirements, constraints, or design notes inside the conversation.
2. The agent MUST treat initial context as a draft input and MUST NOT skip the interview because context was provided.
3. The agent MUST retrieve the canonical job template using `node <skill-local-folder>/graph-engineering/scripts/read-job-template.mjs` (or a equivalent node binary call), or by reading `<skill-local-folder>/graph-engineering/templates/job-template.md`.

- Starting with the next stage, the agent MUST behave as a state machine where each named process section is the current execution state until that section is explicitly completed.
- The default transition condition between states MUST be explicit user confirmation, either by asking for confirmation or by recognizing the user's explicit agreement to proceed.

**2. Interview Purpose, Inputs, and Outputs**

1. The agent MUST ask or confirm what inputs the job may receive.
2. The agent MUST ask or confirm what outputs the job must produce.
3. The agent MUST ask or confirm what the job is responsible for accomplishing.

**3. Interview Process**

1. The agent MUST propose the job process as a sequence of concrete actions.
2. The agent MUST identify which actions are mandatory and which actions are conditional.
3. The agent MUST identify whether the process requires a script.
4. If a script is required, the job process MUST describe when the script is used and what responsibility it serves in one single step.

- The job process MUST NOT duplicate the internal algorithm of the script as numbered job steps.
- Script invocation steps should include script invocation examples in code blocks.
- Script invocation examples in the designed job MUST use `<local-skill-folder>/` for skill-relative paths and MUST NOT hardcode repository-specific skill directories such as `.codex/skills/`.

**4. Resolve Name**

1. The agent SHOULD propose a kebab-case job name when no name was provided or when another kebab-case name appears to be a better option.
2. The agent MUST confirm the final kebab-case job name and human-readable title before generating the design.
3. The agent MUST use the final kebab-case job name as domain.

**5. Generate Outputs**

1. The agent MUST use the canonical job template to compile the conversation with the user into the designed job definition.

- This state MUST NOT require user validation before transitioning to the next state.

**6. Add Script Pseudocode**

1. If the designed job requires a script, the agent MUST write the script as a `.mjs` file.
2. If the designed job requires a script, the agent MUST include script pseudocode in the output as a **Script Pseudocode** output category inside a ## SCRIPTS section after ## Process.
3. The script pseudocode MUST be written inside a code block.
4. The script pseudocode MUST describe the script algorithm, inputs, outputs, error cases, and side effects.
5. The script SHOULD reuse path and graph-engineering helpers from `<skill-local-folder>/graph-engineering/scripts/lib` when resolving local graph-engineering paths.

Example:

```text
Script Pseudocode

INPUT designed_job_data
INPUT output_path

RESOLVE graph_engineering_paths using helpers from <skill-local-folder>/graph-engineering/scripts/lib

IF designed_job_data is missing required fields
  REPORT structured error
  EXIT failure
END IF

BUILD script_output from designed_job_data

WRITE script_output to output_path as .mjs

REPORT output_path
EXIT success
```

**7. Validate and Autocorrect the Design**

1. The agent MUST verify that the designed `JOB.md` follows the canonical job template.
2. The agent MUST verify that the design avoids unnecessary repetition.
3. The agent MUST verify that the process uses categories when categories make the process clearer.
4. The agent MUST verify that numbered process steps are concrete actions.
5. The agent MUST compact steps that are too granular.
6. The agent MUST separate steps that combine distinct actions.
7. The agent MUST move step's notes, rules, and criteria into bullets under the relevant action instead of treating them as numbered steps.

- This validation step MUST be treated as an autocorrection pass. The agent SHOULD already apply these rules while drafting and MUST correct any remaining violations before delivering the Managed Output.
- This state MUST NOT require user validation before transitioning to the next state.

**8. Add Local Designed Job Prompt Example**

1. The agent MUST add a special prompt example under the designed job's `## Prompt examples` section when the designed job is still executed from a local Managed Output.
2. The special prompt example MUST follow the next template for local designed jobs, replacing placeholders with the actual job name and required inputs.

Prompt example Example:

```txt
Execute the <job-name> job in two sequential steps:
1. Load its definition into context by running `design-job` in Latest mode with domain <job-name>.
2. Immediately proceed to execute <job-name> in Default mode using the loaded process.

Inputs for <job-name> job:
- [job-specific input or representative input]
```

- This state MUST NOT require user validation before transitioning to the next state.

## Output

The job MUST produce a Managed Output as a Markdown document containing the designed job.

If the designed job requires a script, the job MUST also produce a local Managed Output with `.mjs` extension containing script pseudocode or script design.

Example relative output paths:

```txt
.graph-engineering/runs/<job-name>/design-job/OUTPUT-<YYYYMMDD-HHMM>.md
.graph-engineering/runs/<job-name>/design-job/<script-name>-<YYYYMMDD-HHMM>.mjs
```

Output generation, serialization, and formatting are executed manually by the agent.

**Markdown Document Output**

The manage markdown document output should follow the canonical job template.

```md
# <Designed Job Title>

## Objective

...

## Inputs

...

## Process

...

## Output

...

## Prompt examples

...
```

**Optional Script Managed Output**

```txt
.graph-engineering/runs/<job-name>/design-job/<script-name>-<timestamp>.mjs
```

**Context Output Extension**

In addition to the mandatory links for generated artifacts, the Context Output MUST report:

- The final proposed job name and title;
- A trial prompt example that loads `design-job` in Latest mode with the final job name as the domain when the design has not been migrated into the main jobs repository.

On successful completion, the agent MUST report the Managed Output links and summarize the design decisions.

On failure, the agent MUST report the missing interview information, unresolved naming issue, output path issue, or template validation issue.

## Prompt examples

```txt
Execute the design-job job to design a job named infer-initiatives.
```


```txt
Execute the <job-name> job in two sequential steps:
1. Load its definition into context by running `design-job` in Latest mode with domain <job-name>.
2. Immediately proceed to execute <job-name> in Default mode using the loaded process.

Inputs for <job-name> job:
- [job-specific input or representative input]
```
