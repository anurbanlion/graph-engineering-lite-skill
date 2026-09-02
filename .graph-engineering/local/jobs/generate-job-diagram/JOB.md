# Generate Job Diagram

## Objective

The job MUST validate a required job identifier, resolve its local path, determine whether a current `GRAPH.json` exists, and generate or update the local Mermaid diagram through the colocated `GRAPH.json` process.

The job MUST NOT modify the target job's `GRAPH.json` or retry a failed validation or generation.

## Inputs

The job MUST receive:

- `target_job_name`: the required target job identifier whose graph should be inspected.

## Scope

The agent MAY inspect:

```txt
.graph-engineering/local/jobs/
.graph-engineering/local/scripts/
```

The agent MAY modify:

```txt
.graph-engineering/local/jobs/<resolved-job-path>/GRAPH.md
```

The agent MUST NOT modify the target `GRAPH.json` or unrelated jobs.

## Process

Execution MUST be delegated to the colocated `GRAPH.json`. The graph MUST infer and validate `target_job_name` from the conversation and prompt with `check_graph`, propagate the validated `target_job_name` and `job_path`, and invoke `generate_job_mermaid` to resolve the current graph and delegate Mermaid conversion to `graph_to_mermaid`.

## Output

The job MUST produce or update the target job's `GRAPH.md` as a Project Output when a graph is available. It MUST produce no diagram when validation reports that the target job has no graph. Output generation MUST be deterministic through the scripts invoked by `GRAPH.json`.

On successful completion, the agent MUST report the target job identifier, resolved job path, and generated `GRAPH.md` path.

On failure, the agent MUST report the failing job identifier, the failed graph state, and the error context.

## Prompt examples

```txt
Execute the job `generate-job-diagram` with the input `target_job_name=design-job`.
```

```txt
Generate the Mermaid diagram for the local job `manage-tasks`.
```
