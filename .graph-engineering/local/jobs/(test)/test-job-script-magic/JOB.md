# Test Job Script Magic

> Version: 1.0
> Location: `graph-engineering/jobs/test-job-script-magic/JOB.md`

## Objective

The job MUST generate an automated environment diagnostic snapshot report for a given domain using a deterministic script.

## Inputs

The job MAY receive:

- a target `domain` parameter.

Examples:

```txt
Execute the test-job-script-magic job for domain staging.
```

```txt
Execute test-job-script-magic.
```

## Process

1. The agent MUST request the target `domain` from the user if it was not provided in the request context.
2. The agent MUST resolve the destination Managed Output path using `resolve_output_path.py`:
   ```bash
   python3 <local-skill-folder>/graph-engineering/scripts/resolve_output_path.py <domain> test-job-script-magic
   ```
3. The agent MUST invoke the generation script passing the resolved output path directly to create the artifact:
   ```bash
   node <local-skill-folder>/graph-engineering/scripts/custom/generate-script-magic-output.mjs <resolved-output-path>
   ```

## SCRIPTS

### Script Pseudocode

```text
Script Pseudocode

INPUT resolved_output_path

IF resolved_output_path is missing
  REPORT structured error "Missing target output path"
  EXIT failure
END IF

COLLECT environment_metrics, timestamp, and host_info

BUILD diagnostic_report_content:
  HEADER "Environment Diagnostic Snapshot"
  SECTION "System Status and Metrics"
  TIMESTAMP current_iso_timestamp

WRITE diagnostic_report_content TO resolved_output_path

REPORT resolved_output_path
EXIT success
```

## Output

The job MUST produce a Managed Output as a Markdown document containing the environment diagnostic snapshot.

Output generation, serialization and formatting are executed deterministically by script.

**Markdown Document Output**

```md
# Environment Diagnostic Snapshot

## System Status and Metrics

- **Timestamp**: <ISO-8601>
- **Domain**: <domain>
- **Status**: Ready
```

On successful completion, the agent MUST report the generated artifact path.

On failure, the agent MUST report the script execution error or path resolution failure.

## Prompt examples

```txt
Execute the test-job-script-magic job.
```

```txt
Execute the test-job-script-magic job in two sequential steps:
1. Load its definition into context by running `design-job` in Latest mode with domain test-job-script-magic.
2. Immediately proceed to execute test-job-script-magic in Default mode using the loaded process.

Inputs for test-job-script-magic job:
- domain: staging
```
