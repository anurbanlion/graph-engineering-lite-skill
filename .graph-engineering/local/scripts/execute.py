#!/usr/bin/env python3

from __future__ import annotations

import copy
import json
import os
import re
import shlex
import subprocess
import sys
import tempfile
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal, Mapping

from lib.errors import fail
from lib.execute_models import (
    Context,
    ExecutionMode,
    ExistingTransitionInput,
    FinalStateDefinition,
    InitialTransitionInput,
    InstructionStateDefinition,
    RuntimePayload,
    ScriptStateDefinition,
    Snapshot,
    SpawnStateDefinition,
    StateDefinition,
    StateKind,
    SwitchStateDefinition,
    Transition,
    TransitionDefinition,
    TransitionInput,
)
from lib.paths import RUNTIME_RELATIVE_PATH, get_project_root
from lib.resolve_job import JobResolutionError, resolve_job
from lib.resolve_script import ScriptResolutionError, resolve_script


INVOCATION_PROJECT_ROOT = get_project_root()
SNAPSHOT_DIR = INVOCATION_PROJECT_ROOT / RUNTIME_RELATIVE_PATH
EXECUTE_PATH = Path(__file__).resolve()
VALID_EXECUTION_MODES = {"default", "echo", "latest", "iterative"}
CONTEXT_REFERENCE_PATTERN = re.compile(
    r"\{context\.(?P<key>[A-Za-z_][A-Za-z0-9_]*)\}"
)

Graph = dict[str, Any]


@dataclass(frozen=True)
class NewExecutionInputs:
    execution_type: Literal["new"]
    job_name: str
    project_root: str
    execution_mode: ExecutionMode
    parent_id: str | None
    context_updates: Context


@dataclass(frozen=True)
class ExistingExecutionInputs:
    execution_type: Literal["existing"]
    execution_id: str
    transition_event: str
    context_updates: Context


CommandInputs = NewExecutionInputs | ExistingExecutionInputs


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def parse_context_entry(value: str) -> tuple[str, str]:
    if "=" not in value:
        fail(f"Invalid format for --context, expected key=value but got: {value}")
    key, context_value = value.split("=", 1)
    if not key:
        fail("Invalid format for --context; key must not be empty.")
    return key, context_value


def read_option_value(
    argv: list[str],
    index: int,
    option: str,
) -> tuple[str, int] | None:
    token = argv[index]
    prefix = f"{option}="
    if token.startswith(prefix):
        value = token[len(prefix):]
        if not value:
            fail(f"Missing value for {option}.")
        return value, index + 1
    if token == option:
        if index + 1 >= len(argv):
            fail(f"Missing value for {option}.")
        return argv[index + 1], index + 2
    return None


def parse_new_execution_inputs(argv: list[str]) -> NewExecutionInputs:
    if len(argv) < 3:
        fail("Missing job name after --job flag.")

    job_name = argv[2]
    project_root = ""
    execution_mode: ExecutionMode = "default"
    parent_id: str | None = None
    context_updates: Context = {}
    index = 3

    while index < len(argv):
        parsed = read_option_value(argv, index, "--project-root")
        if parsed is not None:
            project_root, index = parsed
            continue

        parsed = read_option_value(argv, index, "--execution-mode")
        if parsed is not None:
            execution_mode_value, index = parsed
            execution_mode = execution_mode_value  # type: ignore[assignment]
            continue

        parsed = read_option_value(argv, index, "--parent-id")
        if parsed is not None:
            parent_id, index = parsed
            continue

        parsed = read_option_value(argv, index, "--context")
        if parsed is not None:
            context_entry, index = parsed
            key, value = parse_context_entry(context_entry)
            context_updates[key] = value
            continue

        fail(f"Invalid initialization argument: {argv[index]}")

    return NewExecutionInputs(
        execution_type="new",
        job_name=job_name,
        project_root=project_root,
        execution_mode=execution_mode,
        parent_id=parent_id,
        context_updates=context_updates,
    )


def parse_existing_execution_inputs(argv: list[str]) -> ExistingExecutionInputs:
    if len(argv) < 3:
        fail(usage())

    context_updates: Context = {}
    index = 3
    while index < len(argv):
        parsed = read_option_value(argv, index, "--context")
        if parsed is None:
            fail(f"Invalid continuation argument: {argv[index]}")
        context_entry, index = parsed
        key, value = parse_context_entry(context_entry)
        context_updates[key] = value

    return ExistingExecutionInputs(
        execution_type="existing",
        execution_id=argv[1],
        transition_event=argv[2],
        context_updates=context_updates,
    )


def parse_command_line_inputs(argv: list[str]) -> CommandInputs:
    if len(argv) < 2:
        fail(usage())
    if argv[1] == "--job":
        return parse_new_execution_inputs(argv)
    return parse_existing_execution_inputs(argv)


def validate_inputs(inputs: CommandInputs) -> None:
    if inputs.execution_type == "new":
        if not inputs.job_name:
            fail("A job name is required to start an execution.")
        if not inputs.project_root:
            fail("--project-root is required to start an execution.")
        project_root = Path(inputs.project_root).expanduser()
        if not project_root.is_absolute():
            fail("--project-root must be an absolute path.")
        resolved_project_root = project_root.resolve()
        if not resolved_project_root.is_dir() or not (
            resolved_project_root / ".codex"
        ).is_dir():
            fail("--project-root must identify a project containing .codex.")
        if inputs.execution_mode not in VALID_EXECUTION_MODES:
            fail(
                f"Invalid execution mode '{inputs.execution_mode}'. "
                f"Valid modes: {sorted(VALID_EXECUTION_MODES)}"
            )
        if inputs.parent_id:
            validate_execution_id(inputs.parent_id)
        return

    validate_execution_id(inputs.execution_id)
    if not inputs.transition_event:
        fail("A transition event is required to continue an execution.")


def usage() -> str:
    return (
        "Usage:\n"
        "  execute.py --job <job-name> --project-root <absolute-path> "
        "[--execution-mode <mode>] [--parent-id <id>] "
        "[--context key=value ...]\n"
        "  execute.py <execution-id> <event> [--context key=value ...]"
    )


def load_graph(path: Path) -> Graph:
    try:
        with path.open(encoding="utf-8") as file:
            graph = json.load(file)
    except OSError as error:
        fail(f"Unable to read {path.name}: {error}")
    except json.JSONDecodeError as error:
        fail(f"{path.name} contains invalid JSON: {error}")

    if not isinstance(graph, dict):
        fail(f"{path.name} must contain one JSON object.")
    if not isinstance(graph.get("initial"), str):
        fail("GRAPH.json does not define a valid 'initial' state name.")
    if not isinstance(graph.get("states"), dict):
        fail("GRAPH.json does not define a valid 'states' object.")
    if graph["initial"] not in graph["states"]:
        fail(f"Initial state '{graph['initial']}' does not exist in graph.states.")
    return graph


def load_job_graph(job_name: str, project_root: str | Path) -> Graph:
    try:
        resolved_job = resolve_job(job_name, Path(project_root))
    except JobResolutionError as error:
        fail(str(error))

    graph_path = resolved_job.graph_json_path
    if graph_path is None:
        fail(
            f"GRAPH.json not found for job '{job_name}'. "
            "Cannot execute as a state machine."
        )
    return load_graph(graph_path)


def load_job_graph_from_snapshot(snapshot: Snapshot) -> Graph:
    return load_job_graph(snapshot.machine_name, snapshot.project_root)


def process_new_execution_inputs(
    inputs: NewExecutionInputs,
) -> tuple[Graph, InitialTransitionInput]:
    project_root = str(Path(inputs.project_root).expanduser().resolve())
    graph = load_job_graph(inputs.job_name, project_root)
    transition_input = InitialTransitionInput(
        machine_name=inputs.job_name,
        project_root=project_root,
        execution_mode=inputs.execution_mode,
        context_updates=inputs.context_updates,
        parent_id=inputs.parent_id,
    )
    return graph, transition_input


def process_existing_execution_inputs(
    inputs: ExistingExecutionInputs,
) -> tuple[Graph, ExistingTransitionInput]:
    snapshot = get_current_snapshot(inputs.execution_id)
    graph = load_job_graph_from_snapshot(snapshot)
    transition_input = ExistingTransitionInput(
        snapshot=snapshot,
        event=inputs.transition_event,
        context_updates=inputs.context_updates,
    )
    return graph, transition_input


def create_execution_id() -> str:
    return f"exec-{uuid.uuid4().hex[:8]}"


def validate_execution_id(execution_id: str) -> None:
    if not execution_id.startswith("exec-"):
        fail("Invalid execution-id.")
    if not re.fullmatch(r"[A-Za-z0-9_-]+", execution_id):
        fail("Invalid execution-id.")


def snapshot_path(execution_id: str) -> Path:
    validate_execution_id(execution_id)
    return SNAPSHOT_DIR / f"{execution_id}.json"


def transition_from_mapping(raw_transition: Mapping[str, Any]) -> Transition:
    event = raw_transition.get("event")
    from_state = raw_transition.get("from_state", raw_transition.get("from"))
    to_state = raw_transition.get("to_state", raw_transition.get("to"))
    condition = raw_transition.get("condition")
    at = raw_transition.get("at")
    if not all(isinstance(value, str) for value in (event, from_state, to_state, at)):
        fail("Execution snapshot contains an invalid transition.")
    if condition is not None and not isinstance(condition, str):
        fail("Execution snapshot contains an invalid transition condition.")
    return Transition(
        event=event,
        from_state=from_state,
        to_state=to_state,
        condition=condition,
        at=at,
    )


def snapshot_from_mapping(raw_snapshot: Mapping[str, Any]) -> Snapshot:
    execution_id = raw_snapshot.get("execution_id")
    machine_name = raw_snapshot.get("machine_name", raw_snapshot.get("machine"))
    execution_mode = raw_snapshot.get("execution_mode", "default")
    project_root = raw_snapshot.get("project_root")
    context = raw_snapshot.get("context", {})
    state_name = raw_snapshot.get("state_name", raw_snapshot.get("state"))
    parent_id = raw_snapshot.get("parent_id")

    if not all(
        isinstance(value, str)
        for value in (
            execution_id,
            machine_name,
            execution_mode,
            project_root,
            state_name,
        )
    ):
        fail("Execution snapshot is missing required fields.")
    if execution_mode not in VALID_EXECUTION_MODES:
        fail(f"Execution snapshot contains invalid mode '{execution_mode}'.")
    if not isinstance(context, dict) or not all(
        isinstance(key, str) and isinstance(value, str)
        for key, value in context.items()
    ):
        fail("Execution snapshot context must contain string values.")
    if parent_id is not None and not isinstance(parent_id, str):
        fail("Execution snapshot contains an invalid parent id.")

    raw_last_transition = raw_snapshot.get(
        "last_transition",
        raw_snapshot.get("transition", raw_snapshot.get("metadata")),
    )
    last_transition: Transition | None = None
    if isinstance(raw_last_transition, dict) and raw_last_transition.get("event"):
        last_transition = transition_from_mapping(raw_last_transition)

    history: list[Transition] = []
    raw_history = raw_snapshot.get("history", [])
    if not isinstance(raw_history, list):
        fail("Execution snapshot history must be an array.")
    for raw_transition in raw_history:
        if not isinstance(raw_transition, dict):
            fail("Execution snapshot history contains an invalid transition.")
        if raw_transition.get("event"):
            history.append(transition_from_mapping(raw_transition))

    return Snapshot(
        execution_id=execution_id,
        machine_name=machine_name,
        execution_mode=execution_mode,  # type: ignore[arg-type]
        project_root=project_root,
        context=dict(context),
        state_name=state_name,
        last_transition=last_transition,
        history=history,
        parent_id=parent_id,
    )


def get_current_snapshot(execution_id: str) -> Snapshot:
    path = snapshot_path(execution_id)
    if not path.is_file():
        fail(f"Execution '{execution_id}' does not exist.")
    try:
        with path.open(encoding="utf-8") as file:
            raw_snapshot = json.load(file)
    except OSError as error:
        fail(f"Unable to read execution '{execution_id}': {error}")
    except json.JSONDecodeError as error:
        fail(f"Execution memory for '{execution_id}' is corrupted: {error}")
    if not isinstance(raw_snapshot, dict):
        fail(f"Execution memory for '{execution_id}' must be an object.")
    snapshot = snapshot_from_mapping(raw_snapshot)
    if snapshot.execution_id != execution_id:
        fail(f"Execution memory for '{execution_id}' is inconsistent.")
    return snapshot


def normalize_graph_context(graph: Graph) -> Context:
    raw_context = graph.get("context", {})
    if not isinstance(raw_context, dict) or not all(
        isinstance(key, str) and isinstance(value, str)
        for key, value in raw_context.items()
    ):
        fail("GRAPH.json field 'context' must contain string values.")
    return copy.deepcopy(raw_context)


def apply_transition(
    graph: Graph,
    transition_input: TransitionInput,
) -> Snapshot:
    if isinstance(transition_input, InitialTransitionInput):
        context = normalize_graph_context(graph)
        context.update(transition_input.context_updates)
        return Snapshot(
            execution_id=create_execution_id(),
            machine_name=transition_input.machine_name,
            execution_mode=transition_input.execution_mode,
            project_root=transition_input.project_root,
            context=context,
            state_name=graph["initial"],
            last_transition=None,
            history=[],
            parent_id=transition_input.parent_id,
        )

    next_snapshot = copy.deepcopy(transition_input.snapshot)
    next_snapshot.context.update(transition_input.context_updates)
    current_state = get_state_definition(next_snapshot, graph)
    if current_state.type == "final":
        fail(
            f"Execution '{next_snapshot.execution_id}' is already terminal "
            f"in state '{next_snapshot.state_name}'."
        )

    transition_definition = current_state.on.get(transition_input.event)
    if transition_definition is None:
        fail(
            f"Event '{transition_input.event}' is not valid for execution "
            f"'{next_snapshot.execution_id}'. Allowed events: "
            f"{list(current_state.on.keys())}"
        )
    if transition_definition.target not in graph["states"]:
        fail(
            f"Transition '{transition_input.event}' from state "
            f"'{next_snapshot.state_name}' targets unknown state "
            f"'{transition_definition.target}'."
        )

    transition = Transition(
        event=transition_input.event,
        from_state=next_snapshot.state_name,
        to_state=transition_definition.target,
        condition=transition_definition.condition,
        at=now_iso(),
    )
    next_snapshot.state_name = transition.to_state
    next_snapshot.last_transition = transition
    next_snapshot.history.append(transition)
    return next_snapshot


def save_snapshot(snapshot: Snapshot) -> Snapshot:
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    path = snapshot_path(snapshot.execution_id)
    file_descriptor, temporary_path = tempfile.mkstemp(
        prefix=f".{snapshot.execution_id}.",
        suffix=".tmp",
        dir=SNAPSHOT_DIR,
    )
    try:
        with os.fdopen(file_descriptor, "w", encoding="utf-8") as file:
            json.dump(asdict(snapshot), file, indent=2)
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
    return snapshot


def normalize_string_sequence(value: Any, field_name: str) -> tuple[str, ...]:
    if value is None:
        return ()
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        fail(f"State field '{field_name}' must be an array of strings.")
    return tuple(value)


def normalize_transition_definitions(
    value: Any,
) -> dict[str, TransitionDefinition]:
    if value is None:
        return {}
    if not isinstance(value, dict):
        fail("State field 'on' must be an object.")
    transitions: dict[str, TransitionDefinition] = {}
    for event, raw_transition in value.items():
        if not isinstance(event, str) or not isinstance(raw_transition, dict):
            fail("State transitions must map event names to objects.")
        target = raw_transition.get("target")
        condition = raw_transition.get("condition")
        if not isinstance(target, str):
            fail(f"Transition '{event}' does not define a valid target.")
        if condition is not None and not isinstance(condition, str):
            fail(f"Transition '{event}' has an invalid condition.")
        transitions[event] = TransitionDefinition(
            target=target,
            condition=condition,
            instructions=normalize_string_sequence(
                raw_transition.get("instructions"),
                f"on.{event}.instructions",
            ),
        )
    return transitions


def resolve_graph_state_type(raw_state: Mapping[str, Any]) -> StateKind:
    state_type = raw_state.get("type")
    if state_type not in {"instruction", "script", "switch", "spawn", "final"}:
        fail(
            "State field 'type' is required and must be one of: "
            "instruction, script, switch, spawn, final."
        )
    return state_type  # type: ignore[return-value]


def get_state_definition(snapshot: Snapshot, graph: Graph) -> StateDefinition:
    raw_state = graph["states"].get(snapshot.state_name)
    if not isinstance(raw_state, dict):
        fail(
            f"Execution '{snapshot.execution_id}' references unknown state "
            f"'{snapshot.state_name}'."
        )
    state_type = resolve_graph_state_type(raw_state)
    transitions = normalize_transition_definitions(raw_state.get("on"))
    common = {
        "name": snapshot.state_name,
        "type": state_type,
        "on": transitions,
    }

    if state_type == "script":
        raw_exit_codes = raw_state.get("exit_codes", {})
        if not isinstance(raw_exit_codes, dict) or not all(
            isinstance(code, str) and isinstance(event, str)
            for code, event in raw_exit_codes.items()
        ):
            fail("Script state field 'exit_codes' must map strings to strings.")
        return ScriptStateDefinition(
            **common,
            scripts=normalize_string_sequence(raw_state.get("scripts"), "scripts"),
            exit_codes=dict(raw_exit_codes),
        )
    if state_type == "switch":
        switch = raw_state.get("switch")
        if not isinstance(switch, str) or not switch:
            fail("Switch state must define a non-empty 'switch' field.")
        return SwitchStateDefinition(**common, switch=switch)
    if state_type == "spawn":
        spawn = raw_state.get("spawn")
        if not isinstance(spawn, str) or not spawn:
            fail("Spawn state must define a non-empty 'spawn' command.")
        return SpawnStateDefinition(**common, spawn=spawn)
    if state_type == "final":
        if transitions:
            fail("Final state must not define transitions.")
        result = raw_state.get("result")
        if result is None and snapshot.state_name == "complete":
            result = "DONE"
        if result is None and snapshot.state_name == "abort":
            result = "ERROR"
        if not isinstance(result, str) or not result:
            fail("Final state must define a non-empty 'result' event.")
        return FinalStateDefinition(**common, result=result)
    return InstructionStateDefinition(
        **common,
        instructions=normalize_string_sequence(
            raw_state.get("instructions"),
            "instructions",
        ),
    )


def resolve_state_kind(state_definition: StateDefinition) -> StateKind:
    return state_definition.type


def interpolate_command(command: str, snapshot: Snapshot) -> str:
    def replace_reference(match: re.Match[str]) -> str:
        reference = match.group(0)
        key = match.group("key")
        if key not in snapshot.context:
            fail(
                f"Command context reference '{reference}' does not exist "
                "in the current snapshot."
            )
        return snapshot.context[key]

    interpolated_command = CONTEXT_REFERENCE_PATTERN.sub(replace_reference, command)
    interpolated_command = interpolated_command.replace(
        "{project_root}", snapshot.project_root
    )
    if "{" in interpolated_command or "}" in interpolated_command:
        fail(
            "Invalid command interpolation. Only '{project_root}' and "
            "'{context.<field>}' references are supported."
        )
    return interpolated_command


def execute_script(
    state_definition: ScriptStateDefinition,
    snapshot: Snapshot,
) -> int:
    last_exit_code = 0
    for script_command in state_definition.scripts:
        formatted_command = interpolate_command(script_command, snapshot)
        command_parts = shlex.split(formatted_command)
        if not command_parts:
            fail("Script state contains an empty command.")
        script_identifier, *arguments = command_parts
        try:
            resolved_script = resolve_script(
                script_identifier,
                Path(snapshot.project_root),
            )
        except ScriptResolutionError as error:
            fail(str(error))
        result = subprocess.run(
            [sys.executable, str(resolved_script.script_path), *arguments],
            cwd=snapshot.project_root,
        )
        last_exit_code = result.returncode
        if state_definition.exit_codes or last_exit_code != 0:
            return last_exit_code
    return last_exit_code


def resolve_script_transition_event(
    state_definition: ScriptStateDefinition,
    exit_code: int,
) -> str:
    if state_definition.exit_codes:
        return state_definition.exit_codes.get(str(exit_code), "ERROR")
    return "DONE" if exit_code == 0 else "ERROR"


def evaluate_switch(
    state_definition: SwitchStateDefinition,
    snapshot: Snapshot,
) -> str:
    value: Any = snapshot
    for part in state_definition.switch.split("."):
        if isinstance(value, Snapshot):
            if not hasattr(value, part):
                fail(f"Could not resolve switch key '{state_definition.switch}'.")
            value = getattr(value, part)
        elif isinstance(value, dict):
            if part not in value:
                fail(f"Could not resolve switch key '{state_definition.switch}'.")
            value = value[part]
        else:
            fail(f"Could not resolve switch key '{state_definition.switch}'.")
    if not isinstance(value, str):
        fail(
            f"Switch key '{state_definition.switch}' resolved to "
            f"non-string value: {value}"
        )
    if value not in state_definition.on:
        fail(
            f"Switch value '{value}' from '{state_definition.switch}' has no "
            f"matching transition in state '{snapshot.state_name}'."
        )
    return value


def has_option(arguments: list[str], option: str) -> bool:
    return any(
        argument == option or argument.startswith(f"{option}=")
        for argument in arguments
    )


def reject_spawn_managed_options(arguments: list[str]) -> None:
    for option in ("--job", "--project-root", "--parent-id"):
        if has_option(arguments, option):
            fail(f"Spawn command must not override runtime-managed option {option}.")


def start_child_runtime(
    state_definition: SpawnStateDefinition,
    snapshot: Snapshot,
) -> int:
    command_parts = shlex.split(interpolate_command(state_definition.spawn, snapshot))
    if not command_parts:
        fail("Spawn state contains an empty command.")
    child_job, *arguments = command_parts
    reject_spawn_managed_options(arguments)

    command = [
        sys.executable,
        str(EXECUTE_PATH),
        "--job",
        child_job,
        "--project-root",
        snapshot.project_root,
        "--parent-id",
        snapshot.execution_id,
    ]
    command.extend(arguments)
    return subprocess.run(command, cwd=snapshot.project_root).returncode


def build_runtime_payload(
    snapshot: Snapshot,
    state_definition: StateDefinition,
) -> RuntimePayload:
    return RuntimePayload(
        execution_id=snapshot.execution_id,
        machine_name=snapshot.machine_name,
        execution_mode=snapshot.execution_mode,
        context=dict(snapshot.context),
        state=state_definition,
        last_transition=snapshot.last_transition,
        parent_id=snapshot.parent_id,
    )


def print_runtime_payload(
    snapshot: Snapshot,
    state_definition: StateDefinition,
) -> None:
    print(json.dumps(asdict(build_runtime_payload(snapshot, state_definition)), indent=2))


def resume_parent_runtime(
    snapshot: Snapshot,
    state_definition: FinalStateDefinition,
) -> None:
    if snapshot.parent_id is None:
        fail("Cannot resume a parent runtime without parent_id.")
    result = subprocess.run(
        [
            sys.executable,
            str(EXECUTE_PATH),
            snapshot.parent_id,
            state_definition.result,
        ],
        cwd=snapshot.project_root,
    )
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def drive_runtime(snapshot: Snapshot, graph: Graph) -> None:
    current_snapshot = snapshot
    while True:
        current_snapshot = save_snapshot(current_snapshot)
        state_definition = get_state_definition(current_snapshot, graph)
        state_kind = resolve_state_kind(state_definition)

        if state_kind == "script":
            exit_code = execute_script(state_definition, current_snapshot)
            event = resolve_script_transition_event(state_definition, exit_code)
            current_snapshot = apply_transition(
                graph,
                ExistingTransitionInput(current_snapshot, event, {}),
            )
            continue

        if state_kind == "switch":
            event = evaluate_switch(state_definition, current_snapshot)
            current_snapshot = apply_transition(
                graph,
                ExistingTransitionInput(current_snapshot, event, {}),
            )
            continue

        if state_kind == "spawn":
            exit_code = start_child_runtime(state_definition, current_snapshot)
            if exit_code != 0:
                current_snapshot = apply_transition(
                    graph,
                    ExistingTransitionInput(current_snapshot, "ERROR", {}),
                )
                continue
            return

        if state_kind == "final":
            if current_snapshot.parent_id is None:
                print_runtime_payload(current_snapshot, state_definition)
            else:
                resume_parent_runtime(current_snapshot, state_definition)
            return

        print_runtime_payload(current_snapshot, state_definition)
        return


def main() -> None:
    command_inputs = parse_command_line_inputs(sys.argv)
    validate_inputs(command_inputs)
    if command_inputs.execution_type == "new":
        graph, transition_input = process_new_execution_inputs(command_inputs)
    else:
        graph, transition_input = process_existing_execution_inputs(command_inputs)
    snapshot = apply_transition(graph, transition_input)
    drive_runtime(snapshot, graph)


if __name__ == "__main__":
    main()
