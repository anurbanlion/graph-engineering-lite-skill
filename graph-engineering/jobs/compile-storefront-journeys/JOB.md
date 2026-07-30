# Compile Storefront Journeys

## Objective

The job MUST compile the journeys that exist in the current application by inspecting the run directories managed by Graph Engineering Lite.

## Inputs

The job MAY receive a `domain` in which to store its output.

The `domain` MUST be a kebab-case identifier. 

If the user does not explicitly provide a `domain`, the agent MUST use `global-designs`. The agent MUST NOT infer a domain from the job name, application area, or output content.

## Process

1. The agent MUST execute: `node scripts/custom/compile-application-journeys.mjs <output-path>`

The agent MUST NOT inspect the runs directory manually or reproduce the script's internal discovery and formatting flow.

## Output

The document uses the following format when journeys are found:

```md
# Application Journeys

- account
- checkout
- storefront
```

When no matching journey directories exist, the document uses:

```md
# Application Journeys

No journeys found.
```

Formatting and output writing are handled automatically by the script.

# Prompt examples

```txt
Execute the compile-storefront-journeys job.
```

```txt
Execute the compile-storefront-journeys jobusing the domain application-designs.
```
