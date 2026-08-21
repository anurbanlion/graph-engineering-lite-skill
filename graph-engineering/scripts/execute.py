#!/usr/bin/env python3

import json
import sys
from pathlib import Path


GRAPH_PATH = Path(
    ".codex/skills/graph-engineering/jobs/execute-job/GRAPH.json"
)


def load_graph():
    with GRAPH_PATH.open(encoding="utf-8") as file:
        return json.load(file)


def emit_state(
    graph,
    state_name,
    previous_state=None,
    transition=None,
    condition=None,
):
    if state_name not in graph["states"]:
        print(f"Unknown state: {state_name}", file=sys.stderr)
        sys.exit(1)

    state = graph["states"][state_name]

    result = {
        "state": state_name,
        **state,
    }

    if state_name == "abort":
        result["instructions"] = [
            "You MUST tell the user concisely why the runtime failed.",
            "You MUST stop the current execution immediately after reporting the failure.",
            "You MUST NOT attempt alternative actions, fallback strategies, retries, or continue the workflow unless the user explicitly requests a new action.",
            f"Failure occurred while transitioning from state '{previous_state}' via event '{transition}'.",
            f"Condition for failure: {condition}",
        ]

    elif state_name == "complete":
        result["instructions"] = [
            "Tell the user the runtime completed successfully in a concise manner."
        ]

    print(json.dumps(result, indent=2))


def main():
    graph = load_graph()

    # Start execution from the graph's initial state.
    if len(sys.argv) == 1:
        emit_state(graph, graph["initial"])
        return

    if len(sys.argv) != 3:
        print(
            "Usage: execute.py [<current-state> <transition>]",
            file=sys.stderr,
        )
        sys.exit(1)

    current_state = sys.argv[1]
    transition = sys.argv[2]

    if current_state not in graph["states"]:
        print(
            f"Unknown state: {current_state}",
            file=sys.stderr,
        )
        sys.exit(1)

    state = graph["states"][current_state]
    transitions = state.get("on", {})

    if transition not in transitions:
        print(
            f"Unknown transition '{transition}' "
            f"for state '{current_state}'",
            file=sys.stderr,
        )
        sys.exit(1)

    transition_definition = transitions[transition]

    next_state_name = transition_definition["target"]
    condition = transition_definition.get("condition")

    emit_state(
        graph,
        next_state_name,
        previous_state=current_state,
        transition=transition,
        condition=condition,
    )


if __name__ == "__main__":
    main()