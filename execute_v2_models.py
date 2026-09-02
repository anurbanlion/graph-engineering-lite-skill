"""Approved data-model draft for the V2 execute runtime.

The runtime copy lives in `.graph-engineering/local/scripts/lib/execute_models.py`
so it is distributed with the Graph Engineering skill.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal, Mapping, TypeAlias


ExecutionMode = Literal["default", "echo", "latest", "iterative"]
StateKind = Literal["instruction", "script", "switch", "spawn", "final"]
Context = dict[str, str]


@dataclass(frozen=True)
class Transition:
    """A transition that has already been applied to an execution."""

    event: str
    from_state: str
    to_state: str
    condition: str | None
    at: str


@dataclass(frozen=True)
class TransitionDefinition:
    """A transition declared by a state in GRAPH.json."""

    target: str
    condition: str | None = None
    instructions: tuple[str, ...] = ()


# GRAPH.json state example:
# "inspect": {
#   "type": "instruction",
#   "instructions": ["Inspect input."],
#   "on": {"DONE": {"target": "complete"}}
# }
@dataclass(frozen=True)
class BaseStateDefinition:
    """Fields shared by every static state definition in GRAPH.json.

    `name` is currently the object key in `graph.states`; retaining it here
    keeps a loaded definition self-describing. `on` maps events to the
    transitions that this state permits.
    """

    name: str
    type: StateKind
    on: Mapping[str, TransitionDefinition]


# GRAPH.json state example:
# "inspect": {
#   "type": "instruction",
#   "instructions": ["Inspect input."],
#   "on": {"DONE": {"target": "complete"}}
# }
@dataclass(frozen=True)
class InstructionStateDefinition(BaseStateDefinition):
    """A visible state whose sequential instructions are executed by the agent."""

    type: Literal["instruction"]
    instructions: tuple[str, ...] = ()


# GRAPH.json state example:
# "readJob": {
#   "type": "script",
#   "scripts": ["read_job_inputs {context.job_name}"],
#   "on": {"DONE": {"target": "inspect"}}
# }
#
# GRAPH.json state example with exit codes:
# "readJobProcess": {
#   "type": "script",
#   "scripts": ["read_job_process {context.job_name}"],
#   "exit_codes": {"0": "PROCESS_DETECTED", "2": "SUB_MACHINE_DETECTED"},
#   "on": {"PROCESS_DETECTED": {"target": "validateProcess"}}
# }
@dataclass(frozen=True)
class ScriptStateDefinition(BaseStateDefinition):
    """An automatic state that runs each command in `scripts`.

    Each script command includes its own identifier and arguments as one
    string. `exit_codes` optionally maps a process exit code to an event;
    otherwise zero maps to `DONE` and any nonzero result maps to `ERROR`.
    """

    type: Literal["script"]
    scripts: tuple[str, ...] = ()
    exit_codes: Mapping[str, str] = field(default_factory=dict)


# GRAPH.json state example:
# "resolveMode": {
#   "type": "switch",
#   "switch": "execution_mode",
#   "on": {"default": {"target": "readJob"}}
# }
@dataclass(frozen=True)
class SwitchStateDefinition(BaseStateDefinition):
    """An automatic state that selects an event from the value of `switch`.

    `switch` identifies the snapshot value to evaluate. Its resulting string
    MUST match one of the events declared in `on`.
    """

    type: Literal["switch"]
    switch: str = ""


# GRAPH.json state example:
# "spawnJob": {
#   "type": "spawn",
#   "spawn": "hola-job --execution-mode=echo",
#   "on": {"DONE": {"target": "complete"}}
# }
@dataclass(frozen=True)
class SpawnStateDefinition(BaseStateDefinition):
    """An automatic state that starts the child runtime named by `spawn`.

    `spawn` is a child-runtime command string. It MAY include runtime flags
    such as `--execution-mode=echo` or `--context key=value`, using the same
    command-string convention as a script entry.
    """

    type: Literal["spawn"]
    spawn: str = ""


# GRAPH.json state example:
# "complete": {
#   "type": "final",
#   "result": "DONE",
#   "on": {}
# }
@dataclass(frozen=True)
class FinalStateDefinition(BaseStateDefinition):
    """A terminal state whose `result` resumes its parent when one exists."""

    type: Literal["final"]
    result: str = ""


StateDefinition: TypeAlias = (
    InstructionStateDefinition
    | ScriptStateDefinition
    | SwitchStateDefinition
    | SpawnStateDefinition
    | FinalStateDefinition
)


@dataclass
class Snapshot:
    """Persistent dynamic state for one runtime execution.

    `last_transition` is `None` while the execution remains in the initial
    state selected directly from `graph.initial`.
    """

    execution_id: str
    machine_name: str
    execution_mode: ExecutionMode
    project_root: str
    context: Context
    state_name: str
    last_transition: Transition | None
    history: list[Transition]
    parent_id: str | None = None



@dataclass(frozen=True)
class InitialTransitionInput:
    """Inputs used to initialize a snapshot without applying an event."""

    machine_name: str
    project_root: str
    execution_mode: ExecutionMode
    context_updates: Mapping[str, str]
    parent_id: str | None = None


@dataclass(frozen=True)
class ExistingTransitionInput:
    """Inputs used to apply one event to an existing snapshot."""

    snapshot: Snapshot
    event: str
    context_updates: Mapping[str, str]


TransitionInput: TypeAlias = InitialTransitionInput | ExistingTransitionInput
@dataclass(frozen=True)
class RuntimePayload:
    """Derived state returned to the agent; it is never persisted directly."""

    execution_id: str
    machine_name: str
    execution_mode: ExecutionMode
    context: Mapping[str, str]
    state: StateDefinition
    last_transition: Transition | None
    parent_id: str | None = None
