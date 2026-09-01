## Executing graphs

**Graph discovery**

1. The agent MUST execute `node scripts/list-graphs.mjs` before selecting a graph.
2. The agent MUST use the returned relative paths to identify the single graph that best matches the explicit user request.
3. The agent MUST use only the selected graph's logical identifier when calling `read-graphs.mjs` or `validate-graph.mjs`.
4. The agent MUST NOT read any graph definition before selecting its logical identifier.
5. The agent MUST read the selected graph by executing `node scripts/read-graphs.mjs <graph-name>`.

> Note: `read-graphs.mjs` MAY accept multiple graph names, but the agent MUST NOT use that capability in the current workflow.

> Note: If no available graph name reasonably matches the user request, the agent MUST halt execution and inform the user that no suitable graph is available.

> Note: If two listed graph paths share a logical identifier, the agent MUST halt execution and report the ambiguity.

**Graph validation**

6. The agent MUST validate the selected graph by executing `node scripts/validate-graph.mjs <version> <graph-name>` before executing its first job. The `<version>` argument MUST match the `version` field declared in the graph's `GRAPH.json` definition.
7. If graph validation fails, the agent MUST stop the graph execution and inform the user of the validation errors.

**Graph execution**

7. The agent MUST begin execution with the job referenced by `initial`.
8. The agent MUST execute each job according to the `## Executing jobs` section and the additional `instructions` defined for that job in the graph.
9. If a job requires an input that is not available, the agent MUST pause the graph execution, ask the user for the missing input, and resume the same job after receiving it.
10. The agent MUST NOT inspect manually a managed output artifact (i.e. reading a file) to derive a downstream job input, a system for the managed output to be visible on context is already taken into account with managed output modes.
11. After a successful job execution, the agent MUST continue with the job or terminal outcome defined by `onDone`.
12. After a failed job execution, the agent MUST continue with the job or terminal outcome defined by `onError`.
13. Upon successful graph completion, the agent MUST present a consolidated **Context Output** containing file links grouped by producing job for every Project Output modified and Managed Output generated during that graph execution.

## Graph parsing rules

* `name` identifies the graph.
* `version` identifies the graph definition version.
* `example-prompts` MAY contain a non-empty array of non-empty example prompts that show users how to invoke the graph. These are example prompts for user reference and MUST NOT be treated as execution instructions or followed by the agent during graph execution.
* `initial` identifies the first job to execute.
* `jobs` contains the jobs participating in the graph.
* Each key inside `jobs` MUST match an available job logical identifier.
* `instructions` provides additional execution context for a job.
* `onDone` defines the next job or terminal outcome after a successful execution.
* `onError` defines the next job or terminal outcome after a failed execution, a failed execution is a job missing or an error on a custom script.
* `complete` is a terminal outcome that means the graph finished successfully.
* `abort` is a terminal outcome that means the graph MUST stop. The agent MUST explain which job failed and why the graph was aborted.
* A missing required input is not automatically an error. The agent SHOULD ask the user for the missing input and resume execution.
* The graph runner MUST report an invalid graph when `initial`, `onDone`, or `onError` references an unknown job or terminal outcome.
* Inputs, user interaction, output resolution, and output writing remain controlled by each job and the skill workflow.
* Structured standard output is the preferred interface for passing machine-readable values between graph jobs.
* Managed output artifacts MUST NOT be treated as implicit downstream input interfaces.
* The graph MUST NOT duplicate the internal process, inputs, or output format already defined by a job.

### Usage examples

```bash
# List available graphs
$ node scripts/list-graphs.mjs
build-application-use-cases
build-journey-architecture
```

```bash
# Read a single graph definition
$ node scripts/read-graphs.mjs build-application-use-cases
===== GRAPH: build-application-use-cases =====
{
  "name": "build-application-use-cases",
  "version": "1.0",
  "initial": "analyze-journey-use-cases",
  "jobs": {
    "analyze-journey-use-cases": {
      "instructions": [
        "Use <route-journey>-page as the run/<domain> name."
      ],
      "onDone": "compile-storefront-use-cases",
      "onError": "abort"
    },
    "compile-storefront-use-cases": {
      "instructions": [
        "Use global-designs as the run/<domain> name."
      ],
      "onDone": "complete",
      "onError": "abort"
    }
  }
}
===== END GRAPH: build-application-use-cases =====
```

```bash
# Validate a valid graph definition (version must match the graph's declared version)
$ node scripts/validate-graph.mjs 2.0 build-application-use-cases
Graph is valid: build-application-use-cases
Version: 2.0
Definition: /home/user/projects/my-project/graph-engineering/graphs/build-application-use-cases/GRAPH.json
```

```bash
# Validate an invalid graph definition
$ node scripts/validate-graph.mjs 2.0 invalid-graph
Graph validation failed: invalid-graph
- "initial" MUST be a non-empty string.
```
