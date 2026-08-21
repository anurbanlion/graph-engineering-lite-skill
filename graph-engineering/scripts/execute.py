#!/usr/bin/env python3

import json
import os
import sys
import tempfile
import uuid
from datetime import datetime, timezone

from lib.errors import fail
from lib.paths import (
    EXECUTE_JOB_GRAPH_RELATIVE_PATH,
    RUNTIME_RELATIVE_PATH,
    get_project_root,
)

# ---------------------------------------------------------------------
# Project configuration
# ---------------------------------------------------------------------

PROJECT_ROOT = get_project_root()

GRAPH_PATH = PROJECT_ROOT / EXECUTE_JOB_GRAPH_RELATIVE_PATH

MEMORY_DIR = PROJECT_ROOT / RUNTIME_RELATIVE_PATH

# ---------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def validate_graph(graph):
    if "initial" not in graph:
        fail("GRAPH.json does not define 'initial'.")

    if "states" not in graph:
        fail("GRAPH.json does not define 'states'.")

    if graph["initial"] not in graph["states"]:
        fail(f"Initial state '{graph['initial']}' " "does not exist in graph.states.")


def load_graph():
    try:
        with GRAPH_PATH.open(encoding="utf-8") as file:
            graph = json.load(file)

    except OSError as exc:
        fail(f"Unable to read GRAPH.json: {exc}")

    except json.JSONDecodeError as exc:
        fail(f"GRAPH.json contains invalid JSON: {exc}")

    return graph


# ---------------------------------------------------------------------
# Execution IDs
# ---------------------------------------------------------------------


def create_execution_id():
    """
    Generates a short opaque execution ID.

    Example:
        exec-a91f37c8
    """
    return f"exec-{uuid.uuid4().hex[:8]}"


def validate_execution_id(execution_id):
    if not execution_id.startswith("exec-"):
        fail("Invalid execution-id.")

    allowed = set(
        "abcdefghijklmnopqrstuvwxyz" "ABCDEFGHIJKLMNOPQRSTUVWXYZ" "0123456789-_"
    )

    if any(character not in allowed for character in execution_id):
        fail("Invalid execution-id.")


def execution_path(execution_id):
    validate_execution_id(execution_id)

    return MEMORY_DIR / f"{execution_id}.json"


# ---------------------------------------------------------------------
# Execution memory
# ---------------------------------------------------------------------


def load_execution(execution_id):
    path = execution_path(execution_id)

    if not path.is_file():
        fail(f"Execution '{execution_id}' does not exist.")

    try:
        with path.open(encoding="utf-8") as file:
            execution = json.load(file)

    except OSError as exc:
        fail(f"Unable to read execution " f"'{execution_id}': {exc}")

    except json.JSONDecodeError as exc:
        fail(f"Execution memory for " f"'{execution_id}' is corrupted: {exc}")

    if execution.get("execution_id") != execution_id:
        fail(f"Execution memory for " f"'{execution_id}' is inconsistent.")

    if "state" not in execution:
        fail(f"Execution '{execution_id}' " "does not contain a state.")

    return execution


def save_execution(execution):
    """
    Atomically saves execution state.

    A temporary file is written first and then moved over
    the previous execution file with os.replace().
    """
    MEMORY_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    path = execution_path(execution["execution_id"])

    fd, temporary_path = tempfile.mkstemp(
        prefix=f".{execution['execution_id']}.",
        suffix=".tmp",
        dir=MEMORY_DIR,
    )

    try:
        with os.fdopen(
            fd,
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                execution,
                file,
                indent=2,
            )

            file.write("\n")
            file.flush()
            os.fsync(file.fileno())

        os.replace(
            temporary_path,
            path,
        )

    except Exception:
        try:
            os.unlink(temporary_path)
        except OSError:
            pass

        raise


# ---------------------------------------------------------------------
# State output
# ---------------------------------------------------------------------


def emit_state(
    graph,
    execution,
    previous_state=None,
    event=None,
    condition=None,
):
    state_name = execution["state"]

    if state_name not in graph["states"]:
        fail(
            f"Execution '{execution['execution_id']}' "
            f"references unknown state '{state_name}'."
        )

    state_definition = graph["states"][state_name]

    result = {
        "execution_id": execution["execution_id"],
        "state": state_name,
        **state_definition,
    }

    if state_name == "abort":
        result["instructions"] = [
            "You MUST tell the user concisely why the runtime failed.",
            "You MUST stop the current execution immediately after reporting the failure.",
            "You MUST NOT attempt alternative actions, fallback strategies, retries, or continue the workflow unless the user explicitly requests a new action.",
            (
                "Failure occurred while transitioning "
                f"from state '{previous_state}' "
                f"via event '{event}'."
            ),
            f"Condition for failure: {condition}",
        ]

    elif state_name == "complete":
        result["instructions"] = [
            "Tell the user the runtime completed successfully in a concise manner."
        ]

    print(
        json.dumps(
            result,
            indent=2,
        )
    )


# ---------------------------------------------------------------------
# Start execution
# ---------------------------------------------------------------------


def start_execution(graph):
    execution_id = create_execution_id()

    initial_state = graph["initial"]

    timestamp = now_iso()

    execution = {
        "execution_id": execution_id,
        "state": initial_state,
        "metadata": {
            "event": None,
            "from": None,
            "to": initial_state,
            "condition": None,
            "at": timestamp,
        },
        "history": [
            {
                "event": None,
                "from": None,
                "to": initial_state,
                "condition": None,
                "at": timestamp,
            }
        ],
    }

    save_execution(execution)

    emit_state(
        graph,
        execution,
    )


# ---------------------------------------------------------------------
# Continue execution
# ---------------------------------------------------------------------


def continue_execution(
    graph,
    execution_id,
    event,
):
    execution = load_execution(execution_id)

    current_state = execution["state"]

    if current_state not in graph["states"]:
        fail(
            f"Execution '{execution_id}' " f"contains unknown state '{current_state}'."
        )

    if current_state in {"complete", "abort"}:
        fail(
            f"Execution '{execution_id}' "
            f"is already terminal in state "
            f"'{current_state}'."
        )

    state_definition = graph["states"][current_state]

    transitions = state_definition.get(
        "on",
        {},
    )

    if event not in transitions:
        allowed_events = list(transitions.keys())

        fail(
            f"Event '{event}' is not valid for "
            f"execution '{execution_id}'. "
            f"Allowed events: {allowed_events}"
        )

    transition_definition = transitions[event]

    if "target" not in transition_definition:
        fail(
            f"Transition '{event}' from state "
            f"'{current_state}' does not define "
            "'target'."
        )

    next_state = transition_definition["target"]

    condition = transition_definition.get("condition")

    if next_state not in graph["states"]:
        fail(
            f"Transition '{event}' from state "
            f"'{current_state}' targets unknown "
            f"state '{next_state}'."
        )

    timestamp = now_iso()

    execution["state"] = next_state
    execution["metadata"] = {
        "event": event,
        "from": current_state,
        "to": next_state,
        "condition": condition,
        "at": timestamp,
    }
    execution.setdefault("history", []).append(execution["metadata"])

    save_execution(execution)

    emit_state(
        graph,
        execution,
        previous_state=current_state,
        event=event,
        condition=condition,
    )


# ---------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------


def main():
    graph = load_graph()
    validate_graph(graph)

    # -------------------------------------------------------------
    # execute.py
    #
    # Starts a completely new execution.
    # -------------------------------------------------------------

    if len(sys.argv) == 1:
        start_execution(graph)
        return

    # -------------------------------------------------------------
    # execute.py <execution-id> <event>
    #
    # Continues an existing execution.
    # -------------------------------------------------------------

    if len(sys.argv) == 3:
        execution_id = sys.argv[1]
        event = sys.argv[2]

        continue_execution(
            graph,
            execution_id,
            event,
        )

        return

    fail("Usage:\n" "  execute.py\n" "  execute.py <execution-id> <event>")


if __name__ == "__main__":
    main()
