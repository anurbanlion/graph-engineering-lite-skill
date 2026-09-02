"""Data models used by the Graph Engineering execute runtime."""

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


@dataclass(frozen=True)
class BaseStateDefinition:
    """Fields shared by every normalized GRAPH.json state definition."""

    name: str
    type: StateKind
    on: Mapping[str, TransitionDefinition]


@dataclass(frozen=True)
class InstructionStateDefinition(BaseStateDefinition):
    """A visible state whose sequential instructions are executed by the agent."""

    type: Literal["instruction"]
    instructions: tuple[str, ...] = ()


@dataclass(frozen=True)
class ScriptStateDefinition(BaseStateDefinition):
    """An automatic state that runs script command strings."""

    type: Literal["script"]
    scripts: tuple[str, ...] = ()
    exit_codes: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class SwitchStateDefinition(BaseStateDefinition):
    """An automatic state that selects an event from a snapshot value."""

    type: Literal["switch"]
    switch: str = ""


@dataclass(frozen=True)
class SpawnStateDefinition(BaseStateDefinition):
    """An automatic state that starts the child runtime named by `spawn`."""

    type: Literal["spawn"]
    spawn: str = ""


@dataclass(frozen=True)
class FinalStateDefinition(BaseStateDefinition):
    """A terminal state whose result resumes its parent when one exists."""

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
    """Persistent dynamic state for one runtime execution."""

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
