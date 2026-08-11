# Create Job

## Objective

The job MUST generate or refactor a job definition file (`JOB.md`) following the canonical specification.

The job MUST NOT modify existing execution scripts, graph definitions, or unrelated skill assets unless required (e.g. script logic change, name change).

## Inputs

The job MUST receive at least one of the following:

- User description or requirements for a new job;
- Existing draft or legacy job definition (`JOB.md`).

## Process

**1. Context Synthesis & Clarification**

1. The agent MUST execute `node scripts/read-job-template.mjs` or `graph-engineering/templates/job-template.md` to retrieve the canonical job template and inspect the provided inputs.
2. If the user input is ambiguous or incomplete, the agent MUST ask the user clarifying questions regarding required inputs, process steps, scope boundaries, or expected outputs before generating the document.
3. If transforming an existing or legacy job, the agent MUST filter out runtime execution rules (such as Echo/Latest mode definitions) and convert internal reasoning into RFC-style normative requirements. Additionally, if the existing job conflicts with the canonical template, risks losing critical operational information, or lacks required template fields, the agent MUST ask the user clarifying questions before generating the document.

**2. Job Specification Assembly**

1. The agent MUST structure the job definition using RFC-style normative keywords (`MUST`, `MUST NOT`, `SHOULD`, `MAY`).
2. The agent MUST assign a kebab-case directory name and human-readable title.
3. The agent MUST identify whether the job produces Project Output, Managed Output, or both. The agent MUST treat Context Output as mandatory for every successfully completed job and MAY define an extension only when the job must report user-facing information beyond the mandatory artifact links.
4. The agent MUST populate all required sections (`Objective`, `Inputs`, `Process`, `Output`, and `Prompt examples`).

**3. Output Persistence & Validation**

1. The agent MUST write the complete job definition to:
   ```txt
   graph-engineering/jobs/<job-name>/JOB.md
   ```
2. The agent MUST verify that the generated job matches the structure retrieved by `node scripts/read-job-template.mjs` or `graph-engineering/templates/job-template.md`.
3. The agent MUST verify that any Context Output extension supplements the skill-defined artifact links and does not define persistence or a downstream-job handoff.

## Output

The job MUST produce a project code output stored in the repository:

```txt
graph-engineering/jobs/<job-name>/
└── JOB.md
```

In addition to the mandatory artifact links, the Context Output MUST report:

- The created job directory path and file link (`graph-engineering/jobs/<job-name>/JOB.md`);
- A summary of the specified inputs and outputs.

On failure, the agent MUST report the invalid input, missing template, or generation error.

## Prompt examples

```txt
Execute the create-job job to define a new job named validate-api-schemas that inspects OpenAPI specs and verifies TypeScript types.
```

```txt
Execute the create-job job using the legacy JOB.md file at docs/old-jobs/compile-data.md.
```
