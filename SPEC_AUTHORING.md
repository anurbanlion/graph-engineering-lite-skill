# `.spec` authoring conventions

## Purpose

`.spec` files describe the behavioral contract of a component. They are
human-readable BDD documents, not executable Gherkin templates. Tests may
implement the contract separately.

## Document structure

Use this order:

```text
Feature
  Background
  Rule: <one responsibility>
    Scenario: <generic behavior>
      Given ...
      When ...
      Then ...

      Examples:
        | ... |
```

- A `Feature` states the component's overall responsibility.
- `Background` contains stable inputs and defaults shared by all rules.
- A `Rule` owns one responsibility, such as validation, discovery, selection,
  or the final returned state.
- A `Scenario` defines behavior generically. It MUST NOT be written around one
  example value.
- `Examples:` follow a scenario as illustrative data. They are not part of the
  scenario definition and do not turn it into a `Scenario Outline`.

## Scenario language

- Use `Given` for starting conditions, `When` for the operation, and `Then` /
  `And` for the observable result.
- Use a symbolic input such as `<job-identifier>` when the scenario needs to
  name the input. In these `.spec` files it is documentation notation, not a
  parameter-expansion instruction.
- Do not use `Scenario Outline`; scenarios stay generic and examples remain
  illustrative.
- Keep each scenario focused on one outcome. Put distinct outcomes in distinct
  scenarios.

## Examples

Examples MUST use concrete, representative values such as `my-job` rather than
repeating the generic scenario text. Candidate-selection examples use one row
per candidate:

```text
| job identifier | job_md_path                                              | source | resolution   |
| my-job         | project_root/.graph-engineering/local/jobs/my-job/JOB.md | local  | returned     |
| my-job         | skill_root/jobs/(authoring)/my-job/JOB.md                | skill  | not returned |
```

Use `returned`, `not returned`, `invalid`, or `ambiguity error` for the
resolution column as appropriate.

## Identifiers and paths

- Use `<job-identifier>` for the logical job input. Its accepted format belongs
  in the identifier-validation rule.
- Use `job folder path` for a candidate job directory.
- Use `job_md_path`, `graph_json_path`, and `scripts_folder_path` for paths to
  resources inside a job.
- Use `project_root` for the caller's project directory.
- Use `skill_root` for the active Graph Engineering skill directory. It MAY be
  passed by the caller; otherwise the resolver derives it from its own file.
- The local job folder path is:
  `project_root/.graph-engineering/local/jobs/<job-identifier>`.
- Skill job discovery is under `skill_root/jobs/**`. The `**` allows the job
  folder to be directly under `jobs/` or nested in groups.

## Rules for resolver specifications

For a resolver, separate the contract into rules in execution order:

1. Validate the logical identifier.
2. Discover a local candidate job folder path.
3. Discover skill candidate job folder paths and report duplicate matches.
4. Validate that a candidate job folder path contains its required definition.
5. Prioritize a valid local candidate over a valid skill candidate.
6. Describe the complete resolved result and the not-found outcome.

Do not merge discovery with definition validation: discovery finds a folder
path, while validation decides whether that folder is a valid job.

## Returned state

The final resolver scenario states only that it returns a selected result. Its
`Examples:` table documents the returned fields and representative values.
For jobs, use these fields:

```text
identifier
job_folder_path
source
job_md_path
graph_json_path
scripts_folder_path
```

Optional resources remain represented in the result when they exist; required
resources are established by the validation rule.
