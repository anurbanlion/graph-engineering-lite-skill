#!/usr/bin/env python3

import copy
import json
import os
import shlex
import subprocess
import sys
import tempfile
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Literal, Optional

from lib.errors import fail
from lib.paths import (
    RUNTIME_RELATIVE_PATH,
    SKILL_LOCATION,
    find_job_dir,
    get_jobs_dir,
    get_project_root,
)


PROJECT_ROOT = get_project_root()
SNAPSHOT_DIR = PROJECT_ROOT / RUNTIME_RELATIVE_PATH
VALID_EXECUTION_MODES = {"default", "echo", "latest", "iterative"}

Graph = dict[str, Any]
Snapshot = dict[str, Any]
State = dict[str, Any]
StateType = Literal["script", "switch", "other"]


@dataclass(frozen=True)
class NewExecutionInputs:
    execution_type: Literal["new"]
    job_name: str
    execution_mode: str
    parent_id: Optional[str]


@dataclass(frozen=True)
class ExistingExecutionInputs:
    execution_type: Literal["existing"]
    execution_id: str
    transition_event: str
    context_updates: dict[str, str]


CommandInputs = NewExecutionInputs | ExistingExecutionInputs


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def parse_command_line_inputs(argv: list[str]) -> CommandInputs:
    if len(argv) < 2:
        fail(usage())

    if argv[1] == "--job":
        if len(argv) < 3:
            fail("Missing job name after --job flag.")

        job_name = argv[2]
        execution_mode = "default"
        parent_id = None
        index = 3

        while index < len(argv):
            flag = argv[index]
            if flag == "--execution-mode" and index + 1 < len(argv):
                execution_mode = argv[index + 1]
                index += 2
            elif flag == "--parent-id" and index + 1 < len(argv):
                parent_id = argv[index + 1]
                index += 2
            else:
                fail(f"Invalid or incomplete initialization argument: {flag}")

        return NewExecutionInputs(
            execution_type="new",
            job_name=job_name,
            execution_mode=execution_mode,
            parent_id=parent_id,
        )

    if len(argv) < 3:
        fail(usage())

    execution_id = argv[1]
    transition_event = argv[2]
    context_updates: dict[str, str] = {}
    index = 3

    while index < len(argv):
        if argv[index] != "--context" or index + 1 >= len(argv):
            fail(f"Invalid or incomplete argument: {argv[index]}")

        key_value = argv[index + 1]
        if "=" not in key_value:
            fail(
                "Invalid format for --context, expected key=value "
                f"but got: {key_value}"
            )

        key, value = key_value.split("=", 1)
        context_updates[key] = value
        index += 2

    return ExistingExecutionInputs(
        execution_type="existing",
        execution_id=execution_id,
        transition_event=transition_event,
        context_updates=context_updates,
    )


def validate_inputs(inputs: CommandInputs) -> None:
    if inputs.execution_type == "new":
        if not inputs.job_name:
            fail("A job name is required to start an execution.")
        if inputs.execution_mode not in VALID_EXECUTION_MODES:
            fail(
                f"Invalid execution mode '{inputs.execution_mode}'. "
                f"Valid modes: {sorted(VALID_EXECUTION_MODES)}"
            )
        if inputs.parent_id:
            validate_execution_id(inputs.parent_id)
        return

    if not inputs.transition_event:
        fail("A transition event is required to continue an execution.")
    validate_execution_id(inputs.execution_id)


def usage() -> str:
    return (
        "Usage:\n"
        "  execute_v2.py --job <job-name> "
        "[--execution-mode <mode>] [--parent-id <id>]\n"
        "  execute_v2.py <execution-id> <event> "
        "[--context key=value ...]"
    )


def load_graph(path: Any) -> Graph:
    try:
        with path.open(encoding="utf-8") as file:
            graph = json.load(file)
    except OSError as exc:
        fail(f"Unable to read {path.name}: {exc}")
    except json.JSONDecodeError as exc:
        fail(f"{path.name} contains invalid JSON: {exc}")

    if "initial" not in graph:
        fail("GRAPH.json does not define 'initial'.")
    if "states" not in graph:
        fail("GRAPH.json does not define 'states'.")
    if graph["initial"] not in graph["states"]:
        fail(f"Initial state '{graph['initial']}' does not exist in graph.states.")

    return graph


def resolve_and_load_job_graph(job_name: str) -> Graph:
    jobs_dir = get_jobs_dir(PROJECT_ROOT)
    job_dir = find_job_dir(jobs_dir, job_name)
    if job_dir:
        graph_path = job_dir / "GRAPH.json"
        if graph_path.is_file():
            return load_graph(graph_path)

    fail(
        f"GRAPH.json not found for job '{job_name}'. "
        "Cannot execute as a state machine."
    )


def create_execution_id() -> str:
    return f"exec-{uuid.uuid4().hex[:8]}"


def validate_execution_id(execution_id: str) -> None:
    if not execution_id.startswith("exec-"):
        fail("Invalid execution-id.")

    allowed = set(
        "abcdefghijklmnopqrstuvwxyz"
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "0123456789-_"
    )
    if any(character not in allowed for character in execution_id):
        fail("Invalid execution-id.")


def snapshot_path(execution_id: str) -> Any:
    validate_execution_id(execution_id)
    return SNAPSHOT_DIR / f"{execution_id}.json"


def create_initial_snapshot(
    graph: Graph,
    job_name: str,
    execution_mode: str,
    parent_id: Optional[str] = None,
) -> Snapshot:
    initial_state = graph["initial"]
    transition = {
        "event": None,
        "from": None,
        "to": initial_state,
        "condition": None,
        "at": now_iso(),
    }
    snapshot: Snapshot = {
        "execution_id": create_execution_id(),
        "machine": job_name,
        "execution_mode": execution_mode,
        "context": {"job_name": job_name},
        "state": initial_state,
        "metadata": transition,
        "history": [transition.copy()],
    }
    if parent_id:
        snapshot["parent_id"] = parent_id
    return snapshot


def get_current_snapshot(execution_id: str) -> Snapshot:
    path = snapshot_path(execution_id)
    if not path.is_file():
        fail(f"Execution '{execution_id}' does not exist.")

    try:
        with path.open(encoding="utf-8") as file:
            snapshot = json.load(file)
    except OSError as exc:
        fail(f"Unable to read execution '{execution_id}': {exc}")
    except json.JSONDecodeError as exc:
        fail(f"Execution memory for '{execution_id}' is corrupted: {exc}")

    if snapshot.get("execution_id") != execution_id:
        fail(f"Execution memory for '{execution_id}' is inconsistent.")
    if "state" not in snapshot:
        fail(f"Execution '{execution_id}' does not contain a state.")
    return snapshot





def get_job_name_from_snapshot(snapshot: Snapshot) -> str:
    job_name = snapshot.get("machine") or snapshot.get(
        "context", {}
    ).get("job_name")
    if not job_name:
        fail(
            f"Execution '{snapshot['execution_id']}' does not identify its job."
        )
    return job_name


def update_snapshot(
    snapshot: Snapshot,
    graph: Graph,
    transition_event: Optional[str] = None,
    context_updates: Optional[dict[str, str]] = None,
) -> None:
    next_snapshot = copy.deepcopy(snapshot)
    if context_updates:
        next_snapshot.setdefault("context", {}).update(context_updates)

    if transition_event is not None:
        current_state_name = next_snapshot["state"]
        current_state = get_current_state(next_snapshot, graph)

        if current_state_name in {"complete", "abort"}:
            fail(
                f"Execution '{next_snapshot['execution_id']}' is already "
                f"terminal in state '{current_state_name}'."
            )

        transitions = current_state.get("on", {})
        if transition_event in transitions:
            transition_definition = transitions[transition_event]
        elif transition_event == "ERROR":
            transition_definition = {
                "target": "abort",
                "condition": (
                    f"Transition 'ERROR' is not defined in state "
                    f"'{current_state_name}'"
                ),
            }
        else:
            fail(
                f"Event '{transition_event}' is not valid for execution "
                f"'{next_snapshot['execution_id']}'. "
                f"Allowed events: {list(transitions.keys())}"
            )

        if "target" not in transition_definition:
            fail(
                f"Transition '{transition_event}' from state "
                f"'{current_state_name}' does not define 'target'."
            )

        next_state_name = transition_definition["target"]
        if next_state_name not in graph["states"]:
            fail(
                f"Transition '{transition_event}' from state "
                f"'{current_state_name}' targets unknown state "
                f"'{next_state_name}'."
            )

        transition = {
            "event": transition_event,
            "from": current_state_name,
            "to": next_state_name,
            "condition": transition_definition.get("condition"),
            "at": now_iso(),
        }
        next_snapshot["state"] = next_state_name
        next_snapshot["metadata"] = transition
        next_snapshot.setdefault("history", []).append(transition.copy())

        if (
            next_snapshot.get("execution_mode") == "iterative"
            and current_state_name == "printingOutput"
            and transition_event == "RESOLVE_EXECUTION_MODE"
        ):
            next_snapshot["execution_mode"] = "default"

    save_snapshot(next_snapshot)
    current_state = get_current_state(next_snapshot, graph)
    state_type = resolve_state_type(current_state)

    if state_type == "script":
        exit_code = execute_script(current_state, next_snapshot)
        next_event = resolve_transition_event(current_state, exit_code)
        update_snapshot(next_snapshot, graph, next_event)
        return

    if state_type == "switch":
        next_event = evaluate_switch(current_state, next_snapshot)
        update_snapshot(next_snapshot, graph, next_event)
        return

    print_current_state(current_state, next_snapshot)


def save_snapshot(snapshot: Snapshot) -> None:
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    path = snapshot_path(snapshot["execution_id"])
    file_descriptor, temporary_path = tempfile.mkstemp(
        prefix=f".{snapshot['execution_id']}.",
        suffix=".tmp",
        dir=SNAPSHOT_DIR,
    )

    try:
        with os.fdopen(
            file_descriptor,
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(snapshot, file, indent=2)
            file.write("\n")
            file.flush()
            os.fsync(file.fileno())
        os.replace(temporary_path, path)
    except Exception:
        try:
            os.unlink(temporary_path)
        except OSError:
            pass
        raise


def get_current_state(snapshot: Snapshot, graph: Graph) -> State:
    state_name = snapshot["state"]
    if state_name not in graph["states"]:
        fail(
            f"Execution '{snapshot['execution_id']}' references "
            f"unknown state '{state_name}'."
        )
    return graph["states"][state_name]


def resolve_state_type(current_state: State) -> StateType:
    if "scripts" in current_state:
        return "script"
    if "switch" in current_state:
        return "switch"
    return "other"


def execute_script(
    current_state: State,
    snapshot: Snapshot,
) -> int:
    last_exit_code = 0
    context = snapshot.get("context", {})

    for script_command in current_state.get("scripts", []):
        formatted_command = script_command.format(**context)
        command_parts = shlex.split(formatted_command)
        if not command_parts:
            fail("Script state contains an empty command.")

        script_path = command_parts[0]
        arguments = command_parts[1:]
        full_path = str(
            PROJECT_ROOT / SKILL_LOCATION / script_path.lstrip("/")
        )
        result = subprocess.run(
            ["python3", full_path] + arguments,
            cwd=str(PROJECT_ROOT),
        )
        last_exit_code = result.returncode

        if current_state.get("exit_codes") or last_exit_code != 0:
            return last_exit_code

    return last_exit_code


def resolve_transition_event(
    current_state: State,
    exit_code: int,
) -> str:
    transitions = current_state.get("on", {})
    exit_codes = current_state.get("exit_codes")

    if exit_codes:
        transition_event = exit_codes.get(str(exit_code))
        if transition_event in transitions:
            return transition_event
        return "ERROR"

    if exit_code != 0:
        return "ERROR"
    if "DONE" in transitions:
        return "DONE"
    return "ERROR"


def evaluate_switch(
    current_state: State,
    snapshot: Snapshot,
) -> str:
    switch_key = current_state["switch"]
    value: Any = snapshot

    for part in switch_key.split("."):
        if not isinstance(value, dict):
            fail(f"Could not resolve switch key '{switch_key}' at '{part}'.")
        value = value.get(part, {})

    if not isinstance(value, str):
        fail(
            f"Switch key '{switch_key}' resolved to "
            f"non-string value: {value}"
        )
    if value not in current_state.get("on", {}):
        fail(
            f"Switch value '{value}' from '{switch_key}' has no "
            f"matching transition in state '{snapshot['state']}'."
        )
    return value


def print_current_state(
    current_state: State,
    snapshot: Snapshot,
) -> None:
    state_name = snapshot["state"]
    result = {
        "execution_id": snapshot["execution_id"],
        "execution_mode": snapshot.get("execution_mode", "default"),
        "context": snapshot.get("context", {}),
        "state": state_name,
        **current_state,
    }

    if "parent_id" in snapshot:
        result["parent_id"] = snapshot["parent_id"]

    metadata = snapshot.get("metadata", {})
    if state_name == "abort":
        result["instructions"] = result.get("instructions", []) + [
            "You MUST tell the user concisely why the runtime failed.",
            "You MUST stop the current execution immediately after reporting the failure.",
            "You MUST NOT attempt alternative actions, fallback strategies, retries, or continue the workflow unless the user explicitly requests a new action.",
            (
                "Failure occurred while transitioning "
                f"from state '{metadata.get('from')}' "
                f"via event '{metadata.get('event')}'."
            ),
            f"Condition for failure: {metadata.get('condition')}",
        ]
    elif state_name == "complete":
        result["instructions"] = result.get("instructions", []) + [
            "Tell the user the runtime completed successfully in a concise manner."
        ]

    if state_name in {"abort", "complete"} and "parent_id" in snapshot:
        parent_id = snapshot["parent_id"]
        status_event = (
            "SUB_MACHINE_DONE"
            if state_name == "complete"
            else "SUB_MACHINE_FAILED"
        )
        result.setdefault("instructions", []).append(
            "This sub-execution has finished. You MUST resume the parent "
            "execution by running: "
            f"python3 working/scripts/execute_v2.py "
            f"{parent_id} {status_event}"
        )

    print(json.dumps(result, indent=2))


def main() -> None:
    inputs = parse_command_line_inputs(sys.argv)
    validate_inputs(inputs)

    if inputs.execution_type == "new":
        graph = resolve_and_load_job_graph(inputs.job_name)
        snapshot = create_initial_snapshot(
            graph,
            inputs.job_name,
            inputs.execution_mode,
            inputs.parent_id,
        )
        transition_event = None
        context_updates = None
    else:
        snapshot = get_current_snapshot(inputs.execution_id)
        job_name = get_job_name_from_snapshot(snapshot)
        graph = resolve_and_load_job_graph(job_name)
        transition_event = inputs.transition_event
        context_updates = inputs.context_updates

    update_snapshot(
        snapshot,
        graph,
        transition_event,
        context_updates=context_updates,
    )


if __name__ == "__main__":
    main()