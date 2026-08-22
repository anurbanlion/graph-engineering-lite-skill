#!/usr/bin/env python3

import json
import os
import shlex
import subprocess
import sys
import tempfile
import uuid
from datetime import datetime, timezone

from lib.errors import fail
from lib.paths import (
    EXECUTE_JOB_GRAPH_RELATIVE_PATH,
    RUNTIME_RELATIVE_PATH,
    SKILL_LOCATION,
    get_project_root,
)

# ---------------------------------------------------------------------
# Project configuration
# ---------------------------------------------------------------------

PROJECT_ROOT = get_project_root()

GRAPH_PATH = PROJECT_ROOT / EXECUTE_JOB_GRAPH_RELATIVE_PATH

MEMORY_DIR = PROJECT_ROOT / RUNTIME_RELATIVE_PATH

VALID_EXECUTION_MODES = {"default", "echo", "latest", "iterative"}

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


def load_graph(path=None):
    if path is None:
        path = GRAPH_PATH
    try:
        with path.open(encoding="utf-8") as file:
            graph = json.load(file)

    except OSError as exc:
        fail(f"Unable to read {path.name}: {exc}")

    except json.JSONDecodeError as exc:
        fail(f"{path.name} contains invalid JSON: {exc}")

    return graph


def get_graph_for_job(job_name):
    if not job_name:
        return load_graph()
    
    job_dir = PROJECT_ROOT / ".codex" / "skills" / "graph-engineering" / "jobs" / job_name
    specific_graph_path = job_dir / "GRAPH.json"
    
    if specific_graph_path.is_file():
        return load_graph(specific_graph_path)
    
    return load_graph()


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
# Script node execution
# ---------------------------------------------------------------------


def execute_script_node(graph, execution):
    """
    Execute all scripts declared in a script-type node and auto-transition.

    Supports declarative exit code mapping via the "exit_codes" object.
    If unmapped or missing, defaults to 0 -> DONE, non-zero -> ERROR.
    """
    state_name = execution["state"]
    state_definition = graph["states"][state_name]
    scripts = state_definition.get("scripts", [])
    transitions = state_definition.get("on", {})
    exit_codes_map = state_definition.get("exit_codes")

    context = execution.get("context", {})

    for script_cmd in scripts:
        formatted_cmd = script_cmd.format(**context)
        parts = shlex.split(formatted_cmd)
        
        script_rel_path = parts[0]
        args = parts[1:]

        full_path = str(PROJECT_ROOT / SKILL_LOCATION / script_rel_path.lstrip("/"))

        result = subprocess.run(
            ["python3", full_path] + args,
            cwd=str(PROJECT_ROOT),
        )
        
        # Declarative exit code mapping
        if exit_codes_map:
            exit_code_str = str(result.returncode)
            
            if exit_code_str in exit_codes_map:
                event = exit_codes_map[exit_code_str]
                if event in transitions:
                    continue_execution(graph, execution["execution_id"], event)
                    return
            
            # Fallback for unmapped or failed transitions
            if "ERROR" in transitions:
                continue_execution(graph, execution["execution_id"], "ERROR")
                return
            
            # Force abort if ERROR is missing
            execution["state"] = "abort"
            save_execution(execution)
            emit_state(
                graph,
                execution,
                previous_state=state_name,
                event="ERROR",
                condition=f"Unmapped exit code {exit_code_str} and no ERROR transition defined",
            )
            return

        # Legacy / Default behavior (0 = DONE, != 0 = ERROR)
        if result.returncode != 0:
            if "ERROR" in transitions:
                continue_execution(graph, execution["execution_id"], "ERROR")
            else:
                execution["state"] = "abort"
                save_execution(execution)
                emit_state(
                    graph,
                    execution,
                    previous_state=state_name,
                    event="ERROR",
                    condition="Script failed and no ERROR transition defined",
                )
            return

    # All scripts succeeded (default legacy behavior)
    if not exit_codes_map:
        if "DONE" in transitions:
            continue_execution(graph, execution["execution_id"], "DONE")
        else:
            execution["state"] = "abort"
            save_execution(execution)
            emit_state(
                graph,
                execution,
                previous_state=state_name,
                event="DONE",
                condition="Script succeeded but no DONE transition defined",
            )


def execute_switch_node(graph, execution):
    state_name = execution["state"]
    state_definition = graph["states"][state_name]
    switch_key = state_definition["switch"]
    
    parts = switch_key.split(".")
    val = execution
    for p in parts:
        if isinstance(val, dict):
            val = val.get(p, {})
        else:
            fail(f"Could not resolve switch key '{switch_key}' at '{p}'.")
    
    if not isinstance(val, str):
        fail(f"Switch key '{switch_key}' resolved to non-string value: {val}")

    if val in state_definition.get("on", {}):
        continue_execution(graph, execution["execution_id"], val)
    else:
        fail(
            f"Switch value '{val}' (from '{switch_key}') has no "
            f"matching transition in state '{state_name}'."
        )


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

    if "scripts" in state_definition:
        execute_script_node(graph, execution)
        return

    if "switch" in state_definition:
        execute_switch_node(graph, execution)
        return

    result = {
        "execution_id": execution["execution_id"],
        "execution_mode": execution.get("execution_mode", "default"),
        "context": execution.get("context", {}),
        "state": state_name,
        **state_definition,
    }

    if "parent_id" in execution:
        result["parent_id"] = execution["parent_id"]

    if state_name == "abort":
        existing_instructions = result.get("instructions", [])
        result["instructions"] = existing_instructions + [
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
        existing_instructions = result.get("instructions", [])
        result["instructions"] = existing_instructions + [
            "Tell the user the runtime completed successfully in a concise manner."
        ]
        
    # Intercept terminal states to output Call Stack return instructions
    if state_name in {"abort", "complete"} and "parent_id" in execution:
        parent_id = execution["parent_id"]
        status_event = "SUB_MACHINE_DONE" if state_name == "complete" else "SUB_MACHINE_FAILED"
        result["instructions"].append(
            f"This sub-execution has finished. You MUST resume the parent execution by running: "
            f"python3 .codex/skills/graph-engineering/scripts/execute.py {parent_id} {status_event}"
        )

    print(
        json.dumps(
            result,
            indent=2,
        )
    )


# ---------------------------------------------------------------------
# Start execution
# ---------------------------------------------------------------------


def start_execution(graph, job_name, execution_mode="default", parent_id=None):
    execution_id = create_execution_id()

    initial_state = graph["initial"]

    timestamp = now_iso()

    execution = {
        "execution_id": execution_id,
        "execution_mode": execution_mode,
        "context": {"job_name": job_name},
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

    if parent_id:
        execution["parent_id"] = parent_id

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
    context_updates=None,
):
    execution = load_execution(execution_id)

    if context_updates:
        execution.setdefault("context", {}).update(context_updates)

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

    if (
        execution.get("execution_mode") == "iterative"
        and current_state == "printingOutput"
        and event == "RESOLVE_EXECUTION_MODE"
    ):
        execution["execution_mode"] = "default"

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
    if len(sys.argv) < 2:
        fail(
            "Usage:\n"
            "  execute.py --job <job-name> [--execution-mode <mode>] [--parent-id <id>]\n"
            "  execute.py <execution-id> <event> [--context key=value ...]"
        )

    # -------------------------------------------------------------
    # START JOB: execute.py --job <job-name> ...
    # -------------------------------------------------------------
    if sys.argv[1] == "--job":
        if len(sys.argv) < 3:
            fail("Missing job name after --job flag.")
        
        job_name = sys.argv[2]
        execution_mode = "default"
        parent_id = None
        
        # Verify job folder exists
        job_dir = PROJECT_ROOT / ".codex" / "skills" / "graph-engineering" / "jobs" / job_name
        if not job_dir.is_dir():
            fail(f"Job directory '{job_dir}' does not exist.")
            
        # Parse optional flags for initialization
        i = 3
        while i < len(sys.argv):
            flag = sys.argv[i]
            if flag == "--execution-mode" and i + 1 < len(sys.argv):
                execution_mode = sys.argv[i + 1]
                i += 2
            elif flag == "--parent-id" and i + 1 < len(sys.argv):
                parent_id = sys.argv[i + 1]
                i += 2
            else:
                fail(f"Invalid or incomplete argument during initialization: {flag}")

        if execution_mode not in VALID_EXECUTION_MODES:
            fail(
                f"Invalid execution mode '{execution_mode}'. "
                f"Valid modes: {sorted(VALID_EXECUTION_MODES)}"
            )

        graph = get_graph_for_job(job_name)
        validate_graph(graph)
        start_execution(graph, job_name, execution_mode, parent_id)
        return

    # -------------------------------------------------------------
    # CONTINUE EXECUTION: execute.py <execution-id> <event> ...
    # -------------------------------------------------------------
    if len(sys.argv) >= 3:
        execution_id = sys.argv[1]
        event = sys.argv[2]
        
        context_updates = {}
        i = 3
        while i < len(sys.argv):
            if sys.argv[i] == "--context" and i + 1 < len(sys.argv):
                key_value = sys.argv[i+1]
                if "=" in key_value:
                    k, v = key_value.split("=", 1)
                    context_updates[k] = v
                else:
                    fail(f"Invalid format for --context, expected key=value but got: {key_value}")
                i += 2
            else:
                fail(f"Invalid or incomplete argument: {sys.argv[i]}")

        execution_peek = load_execution(execution_id)
        job_name = execution_peek.get("context", {}).get("job_name")
        graph = get_graph_for_job(job_name)
        validate_graph(graph)
        
        continue_execution(
            graph,
            execution_id,
            event,
            context_updates=context_updates,
        )
        return

    fail(
        "Usage:\n"
        "  execute.py --job <job-name> [--execution-mode <mode>] [--parent-id <id>]\n"
        "  execute.py <execution-id> <event> [--context key=value ...]"
    )


if __name__ == "__main__":
    main()
