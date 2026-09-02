# Execute V2 flow

This document describes the execution flow implemented by the V2 executor.

```mermaid
flowchart TB
    start(["Start execute script"]) --> cliStart[/"Input: new job"/]
    start --> cliContinue[/"Input: existing execution"/]

    cliStart --> parse["Parse command line inputs"]
    cliContinue --> parse
    parse --> validateInputs{"Inputs valid"}
    validateInputs -- Yes --> executionType{"New or existing execution"}

    executionType -- New --> processNewInputs["Process new execution inputs"]
    processNewInputs --> jobName[/"Output: job name"/]
    processNewInputs --> projectRoot[/"Output: project root"/]
    processNewInputs --> contextUpdate[/"Output: context update"/]
    processNewInputs --> executionMode[/"Output: execution mode"/]
    processNewInputs --> parentId[/"Output: parent id"/]
    jobName --> loadGraphNew["Load job graph"]
    loadGraphNew --> graphNew[/"Output: graph"/]
    graphNew & jobName & projectRoot & contextUpdate & executionMode & parentId --> newTransitionInputs[/"Output: graph, job name, project root, context update, execution mode, and parent id"/]

    executionType -- Existing --> processExistingInputs["Process existing execution inputs"]
    processExistingInputs --> executionId[/"Output: execution id"/]
    processExistingInputs --> existingTransitionEvent[/"Output: transition event"/]
    processExistingInputs --> existingContextUpdates[/"Output: context updates"/]
    executionId --> getSnapshot["Get current snapshot"]
    getSnapshot --> snapshot[/"Output: current snapshot"/]
    snapshot --> loadGraphSnapshot["Load job graph from snapshot"]
    loadGraphSnapshot --> graphExisting[/"Output: graph"/]
    existingTransitionEvent & existingContextUpdates & snapshot & graphExisting --> existingTransitionInputs[/"Output: graph, current snapshot, transition event, and context updates"/]

    newTransitionInputs --> applyTransition["Apply transition"]
    existingTransitionInputs --> applyTransition

    applyTransition --> nextSnapshot[/"Output: next snapshot"/]
    nextSnapshot --> saveSnapshot["Save snapshot"]
    saveSnapshot --> savedSnapshot[/"Output: snapshot (saved in storage)"/]
    savedSnapshot --> getStateDefinition["Get state definition"]
    getStateDefinition --> stateDefinition[/"Output: state definition"/]
    stateDefinition --> resolveType{"Resolve state kind"}

    resolveType -- Script --> executeScript["Execute script"]
    executeScript --> resolveScriptEvent["Resolve transition event"]
    resolveScriptEvent --> scriptTransitionEvent[/"Output: transition event"/]
    scriptTransitionEvent --> applyTransition

    resolveType -- Switch --> evaluateSwitch["Evaluate switch"]
    evaluateSwitch --> switchEvent[/"Output: transition event"/]
    switchEvent --> applyTransition

    resolveType -- Spawn --> startChild["Start child runtime"]

    resolveType -- Instruction --> printState["Print runtime payload"]

    resolveType -- Final --> hasParent{"Has parent id"}
    hasParent -- No --> printState
    hasParent -- Yes --> resumeParent["Resume parent runtime with final result"]
```

## Runtime semantics

- `applyTransition` MUST create the initial snapshot when it receives a graph, job name, project root, context updates, execution mode, and parent id without an existing snapshot.
- `applyTransition` MUST apply context updates before resolving the transition target, because the target state MAY immediately interpolate a new context value.
- The existing-execution branch MUST load the graph from `snapshot.machine_name`; it MUST NOT expose a separate get-job-name step.
- A `spawn` state MUST keep its parent snapshot in the current spawn state while it starts the child runtime selected by its `spawn` command.
- A spawn state MUST start the child runtime and yield control to it. It MUST NOT print a parent payload or advance the parent when the child starts. When a child reaches a final state with a parent id, the runtime MUST resume that parent automatically with the final state's result event; it MUST NOT require an agent instruction to continue the parent.
- A final state MUST declare its terminal result event, such as `DONE` or `ERROR`. A final execution without a parent id MUST print its final runtime payload.
