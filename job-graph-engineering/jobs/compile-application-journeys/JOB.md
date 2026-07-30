# Compile Application Journeys

## Objective

The job MUST compile the journeys that exist in the current application by inspecting the run directories managed by Graph Engineering Lite.

## Inputs

The job MAY receive a `domain` in which to store its output.

The `domain` MUST be a kebab-case identifier.

If no `domain` is provided, the agent MUST use `global-designs`.

The agent MUST resolve the output path through the standard job execution workflow before executing this job.

## Process

The agent MUST execute:

```bash
node scripts/custom/compile-application-journeys.mjs <output-path>
```

The agent MUST pass the exact path returned by `resolve-output-path.mjs` as `<output-path>`.

The agent MUST NOT inspect the runs directory manually or reproduce the script's internal discovery and formatting flow.

## Output

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

# Prompt examples

```txt
Using the job-graph-engineering local skill, execute the

- compile-application-journeys

job.
```

```txt
Using the job-graph-engineering local skill, execute the

- compile-application-journeys

job using the domain application-designs.
```
