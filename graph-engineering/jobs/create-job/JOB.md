# Create Job

> Location: `graph-engineering/jobs/create-job/JOB.md`

## Objective

The job MUST generate or refactor a job definition file (`JOB.md`) following the canonical specification in `graph-engineering/templates/job-template.md`.

The job MUST NOT modify existing execution scripts, graph definitions, or unrelated skill assets.

## Inputs

The job MUST receive at least one of the following:

- User description or requirements for a new job;
- Existing draft or legacy job definition (`JOB.md`).

> Note: Inputs may originate from user parameters, explicit files, or back-and-forth clarification.

The job MAY receive:

- `domain`: Optional domain identifier for managed output resolution.

## Process

### Option B: Named Stages (Complex Job)

**1. Context Synthesis & Clarification**

1. The agent MUST inspect the provided inputs and read the reference template in `graph-engineering/templates/job-template.md`.
2. If the user input is ambiguous or incomplete, the agent MUST ask the user clarifying questions regarding required inputs, process steps, scope boundaries, or expected outputs before generating the document.
3. If transforming an existing or legacy job, the agent MUST filter out runtime execution rules (such as Echo/Latest mode definitions) and convert internal reasoning into RFC-style normative requirements.

**2. Job Specification Assembly**

1. The agent MUST structure the job definition using RFC-style normative keywords (`MUST`, `MUST NOT`, `SHOULD`, `MAY`).
2. The agent MUST assign a kebab-case directory name and human-readable title.
3. The agent MUST populate all required sections (`Objective`, `Inputs`, `Process`, `Output`, and `Prompt examples`).
4. The agent MUST ensure the `## Output` section specifies the deliverable format (Markdown, repository code, or JSON) without introducing skill-level execution rules.

**3. Output Persistence & Validation**

1. The agent MUST write the complete job definition to:
   ```txt
   graph-engineering/jobs/<job-name>/JOB.md
   ```
2. The agent MUST verify that the generated job matches the structure of `graph-engineering/templates/job-template.md`.

## Output

The job MUST produce a project code output stored in the repository:

```txt
graph-engineering/jobs/<job-name>/
└── JOB.md
```

On successful completion, the agent MUST report:

- The created job directory path and file link (`graph-engineering/jobs/<job-name>/JOB.md`);
- A summary of the specified inputs, process stages, and outputs.

On failure, the agent MUST report the invalid input, missing template, or generation error.

## Prompt examples

```txt
Execute the create-job job to define a new job named validate-api-schemas that inspects OpenAPI specs and verifies TypeScript types.
```

```txt
Execute the create-job job using the legacy JOB.md file at docs/old-jobs/compile-data.md.
```
