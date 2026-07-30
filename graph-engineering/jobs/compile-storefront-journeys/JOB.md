# Compile Storefront Journeys

## Objective

The job MUST compile the journeys that exist in the current application by inspecting the run directories managed by Graph Engineering Lite.

The job MUST expose the compiled journey identifiers through structured standard output for downstream jobs.

## Inputs

The job MAY receive a `domain` in which to store its output.

The `domain` MUST be a kebab-case identifier.

If the user does not explicitly provide a `domain`, the agent MUST use `global-designs`. The agent MUST NOT infer a domain from the job name, application area, or output content.

## Process

The agent MUST execute:

```bash
node scripts/custom/compile-application-journeys.mjs <output-path>
```

The agent MUST NOT inspect the runs directory manually or reproduce the script's internal discovery and formatting flow.

## Output

The managed output document uses the following format when journeys are found:

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

After successfully writing the managed output document, the script MUST print exactly one JSON object to standard output:

```json
{
  "outputPath": "/absolute/path/to/OUTPUT-YYYYMMDD-HHMM.md",
  "journeys": ["account", "checkout", "storefront"]
}
```

The `journeys` array is the supported input handoff for downstream jobs. Downstream jobs MUST NOT open the managed output document to rediscover journey identifiers.

When execution fails, the script MUST print the reason to standard error and exit with a non-zero status code.

# Prompt examples

```txt
Execute the compile-storefront-journeys job.
```

```txt
Execute the compile-storefront-journeys job using the domain application-designs.
```
