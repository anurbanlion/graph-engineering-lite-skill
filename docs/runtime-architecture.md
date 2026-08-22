# Graph Engineering: Runtime Architecture & Jobs

A job is a bounded unit of work that can be executed independently or composed inside a graph. **Every job execution is governed by a Deterministic State Machine (FSM) runtime to eliminate context contamination, prevent hallucinations, and ensure strict normative adherence.**

A job MUST define:

- which inputs it accepts
- the ordered process it follows
- the output it produces

A job SHOULD describe one responsibility. It MUST NOT duplicate the internal workflow of another job or depend on knowledge of unrelated jobs.

## Location

Each job MUST reside in:

```txt
graph-engineering/jobs/<job-name>/JOB.md
```

The directory name MUST be a kebab-case identifier. The document title SHOULD be the human-readable form of that identifier.

A job MAY use a script when deterministic file discovery, transformation, output writing, or validation is required. **Highly complex jobs MAY also provide their own `GRAPH.json` to define custom FSM states and transitions.**

---

## The FSM Runtime

The backbone of Graph Engineering is the Deterministic State Machine runtime (e.g., `execute.py`). It orchestrates job execution by strictly enforcing state transitions, managing context, and dictating when the AI agent should intervene.

### State Management & Context
The runtime maintains a persistent memory payload per execution, tracking the `execution_id`, current `state`, global `execution_mode`, and a protected `context` dictionary. 

Inputs and runtime variables MUST be injected safely into this FSM Context (`execution["context"]`). The runtime exposes these variables exclusively when needed, preventing the agent from hallucinating unrequested context flags.

### Node Types
The runtime minimizes the agent's cognitive load by categorizing states into three types:

1. **Cognitive Nodes:** States that require non-deterministic reasoning. The runtime stops, prints the JIT instructions, and waits for the agent to take action and call the next transition event.
2. **Script Nodes (`"scripts"`):** States that execute deterministic scripts (e.g., fetching files, validating formats). The runtime runs the script and automatically transitions via `DONE` or `ERROR` without consuming an agent turn.
3. **Switch Nodes (`"switch"`):** Pure routing states. The runtime evaluates a JSON property (using dot-notation, e.g., `execution_mode` or `context.domain`) and instantly auto-transitions to the corresponding branch.

### Just-in-Time Instruction Disclosure (JITID)
Instead of feeding the entire job process to the agent at once, the FSM runtime exposes instructions using JITID. The agent only sees the specific instructions required for the currently active state, significantly reducing prompt saturation.

---

## Inputs

Inputs are the information available when the job begins.

They MAY come directly from the user, from the output of a previous job, from explicitly supplied files (code, briefs, images, etc.), or from project exploration when discovery is part of the job.

Additionally, when producing a managed output, a job MUST specify a target domain to locate or place the artifact.

## Process

The process MUST describe how the job transforms its inputs into its output.

A simple job MAY use a short ordered sequence. A job involving exploration, planning, implementation, or validation SHOULD divide the process into ordered named stages.

The process SHOULD NOT attempt to document the agent's internal reasoning.

## Output

The output is the result owned by the job. A job MAY produce Project Output, Managed Output, or both. Every successfully completed job MUST produce Context Output.

- **Project output:** A project output creates or modifies repository files, such as source code, configuration, tests, or generated project structure.
- **Managed output:** A managed output is a persisted artifact produced by a run, which takes the form of a Markdown document. **A job MAY explicitly state that its Managed Output is generated and persisted by a script. In this case, the FSM will automatically skip the agent's output-writing phase.**
- **Context output:** A context output is a non-persisted message directed to the user. It MUST include links to every project file created or modified and every managed artifact generated during the current job execution, grouped by the producing job's logical identifier. If no file artifacts were generated or modified, it MUST say so explicitly.

A job MAY define additional Context Output requirements. They MUST extend the required artifact links and MUST NOT replace them.

### Execution modes

Because a graph MAY require the artifact content in its active execution context or a job must build its output from a previous iteration, a job with a managed output SHOULD support additional execution modes. **The FSM orchestrates these modes deterministically using `switch` nodes, instantly routing the execution without requiring cognitive turns from the agent.**

These modes apply only to Managed Output:

- Managed output - **Echo mode**: Executes the job normally, persists the new Markdown artifact, but also places the complete generated content in the execution context. **If the output is script-managed, the FSM automatically skips execution writing and routes directly to fetching and echoing the latest script output.**
- Managed output - **Latest mode**: Does not execute the job. It **instantly routes** to locate the latest successful managed output for the same job and relevant domain, then places its complete Markdown content in the graph or execution context. Latest mode MUST NOT create a new managed output. If no matching output exists, the operation MUST fail clearly.
- Managed output - **Iterative mode**: Especial execution mode where it runs the job twice, once in latest mode and once in default mode, or echo if the user indicates so.

These execution modes complement the default managed output mode, which MUST only persist the output artifact and present a file link to the user. A graph MAY express these execution modes as job instructions.

## Script and Automation

A job MAY use a script when part of its process benefits from deterministic behavior, such as locating files, validating inputs, transforming content, writing outputs, or retrieving a previous managed output.

As previously mentioned, scripts are first-class citizens of the FSM runtime and can be used to entirely bypass agent intervention for specific states. A job process MAY consist entirely of just executing a script.
