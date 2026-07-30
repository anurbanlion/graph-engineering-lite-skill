# List Application Journeys

## Objective

The job MUST list the journeys that exist in the current application by inspecting the run directories managed by Graph Engineering Lite.

## Inputs

The job MAY receive a `domain` in which to store its output.

The `domain` MUST be a kebab-case identifier.

If no `domain` is provided, the job MUST use `global-designs`.

## Process

1. The agent MUST execute:

```bash
node scripts/custom/list-application-journeys.mjs [domain]
```

2. The agent MUST NOT inspect the runs directory manually.
3. The script MUST resolve the project folder and inspect `.job-graph-engineering/runs`.
4. The script MUST select only directories whose names end with `-journey`.
5. The script MUST remove the `-journey` suffix from every selected directory name.
6. The script MUST sort the resulting journey names alphabetically.
7. The script MUST write the result to the selected domain and print the same journey list to the console.

## Output

The output MUST be a Markdown document named using the standard `OUTPUT-YYYYMMDD-HHMM.md` convention and stored at:

```text
<project-folder>/.job-graph-engineering/runs/<domain>/list-application-journeys/
```

The document MUST use the following format when journeys are found:

```md
# Application Journeys

- account
- checkout
- storefront
```

When no matching journey directories exist, the document MUST use:

```md
# Application Journeys

No journeys found.
```

The script MUST also print the Markdown content and the generated output path to the console.

# Prompt examples

```txt
Using the job-graph-engineering local skill, execute the

- list-application-journeys

job.
```

```txt
Using the job-graph-engineering local skill, execute the

- list-application-journeys

job using the domain application-designs.
```
