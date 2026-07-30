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

The agent MUST execute the custom script once and pass every journey identifier with a repeated `--journey` option.

```bash
node scripts/custom/scaffold-journey-architecture.mjs \
  --journey cart \
  --journey saved \
  --journey account
```

The agent MUST NOT reproduce the script's directory or file creation flow manually.

The script MUST create missing parent directories and missing files.

The script MUST NOT overwrite, modify, truncate, or format existing files.

The script MUST NOT implement use cases, services, repositories, factories, mocks, server functions, or server actions.

## Output

The job MUST ensure the following code structure exists for every journey:

```txt
apis/
└── [journey]/
    ├── index.ts
    ├── application/
    │   └── use-cases/
    │       └── [journey].use-case.ts
    └── infrastructure/
        ├── repository/
        │   ├── [journey].factory.ts
        │   ├── [journey].repository.ts
        │   └── [journey].mock.repository.ts
        └── services/
            ├── [journey].service.const.ts
            └── [journey].service.ts
```

These files are project code outputs. They are not stored as a managed run artifact.

Missing files MUST be created as empty files. Existing files MUST remain unchanged.

When execution succeeds, the script MUST print a concise summary containing the processed journeys, files created, and files already existing.

When nothing needs to be created, the script MUST still succeed.

When execution fails, the script MUST print the reason to standard error and exit with a non-zero status code.

# Prompt examples

```txt
Execute the scaffold-journey-architecture job for these journeys:

- cart
- saved
- account
```

```txt
Execute the scaffold-journey-architecture job using the journeys produced by the previous job.
```
