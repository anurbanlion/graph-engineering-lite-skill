# Scaffold Journey Architecture

## Objective

The job MUST ensure that the required application and infrastructure structure exists for one or more journeys.

The job MUST create missing directories and files.

The job MUST leave existing files unchanged.

## Inputs

The job MUST receive one or more journey identifiers.

Journey identifiers MAY be provided directly by the user or obtained from the output of a previously executed job.

Each journey identifier MUST contain one or more lowercase words separated by hyphens.

Examples:

```txt
cart
saved
account
order-history
```

## Process

The agent MUST execute the custom script once and pass every resolved journey with a repeated `--journey` option.

```bash
node scripts/custom/scaffold-journey-architecture.mjs \
  --journey cart \
  --journey saved \
  --journey account
```

When the journeys come from a previous job, the agent MUST extract the journey identifiers from that job's output before invoking the script.

The agent MUST NOT reproduce the script's directory or file creation flow manually.

For every journey, the script ensures that the following files exist under the project API root:

```txt
apis/[journey]/index.ts
apis/[journey]/infrastructure/services/[journey].service.const.ts
apis/[journey]/infrastructure/services/[journey].service.ts
apis/[journey]/infrastructure/repository/[journey].factory.ts
apis/[journey]/infrastructure/repository/[journey].repository.ts
apis/[journey]/infrastructure/repository/[journey].mock.repository.ts
apis/[journey]/application/use-cases/[journey].use-case.ts
```

The script creates missing parent directories and creates missing files as empty files.

The script MUST NOT overwrite, modify, truncate, or format existing files.

The script MUST NOT implement use cases, services, repositories, factories, mocks, server functions, or server actions.

## Output

The job does not produce an output artifact.

When execution succeeds, the script prints a concise summary containing the processed journeys, files created, and files already existing.

When nothing needs to be created, the script MUST still succeed.

When execution fails, the script prints the reason to standard error and exits with a non-zero status code.

# Prompt examples

```txt
Using the graph-engineering local skill (.codex/skills), execute the scaffold-journey-architecture job for these journeys:

- cart
- saved
- account
```

```txt
Using the journeys produced by the previous job, execute the scaffold-journey-architecture job.
```
