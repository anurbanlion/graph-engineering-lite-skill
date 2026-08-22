#!/usr/bin/env python3

import argparse
import json
import re
from datetime import datetime
from pathlib import Path


# ============================================================
# Configuration
# ============================================================

HIDDEN_EVENTS = {
    "ERROR",
    "AMBIGUOUS",
}

HIDE_ABORT_TRANSITIONS = True

SCRIPT_STATE_STYLE = (
    "fill:#DCEBFF,"
    "stroke:#2563EB,"
    "stroke-width:2px,"
    "color:#111827"
)

SWITCH_STATE_STYLE = (
    "fill:#FEE2E2,"
    "stroke:#DC2626,"
    "stroke-width:2px,"
    "color:#111827"
)

OUTPUT_PREFIX = "GRAPH"
TIMESTAMP_FORMAT = "%Y%m%d-%H%M"


# ============================================================
# Input / output
# ============================================================

def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate a Mermaid Markdown diagram from a GRAPH.json file."
    )

    parser.add_argument(
        "input",
        type=Path,
        help="Path to the input GRAPH.json file.",
    )

    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help=(
            "Directory where the generated Markdown file will be written. "
            "Defaults to docs/diagrams."
        ),
    )

    return parser.parse_args()


def load_graph(path: Path) -> dict:
    if not path.is_file():
        raise FileNotFoundError(f"Graph file does not exist: {path}")

    try:
        with path.open("r", encoding="utf-8") as file:
            graph = json.load(file)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Graph file contains invalid JSON: {exc}"
        ) from exc

    validate_graph(graph)

    return graph


def validate_graph(graph: dict):
    if not isinstance(graph, dict):
        raise ValueError("Graph root must be a JSON object.")

    if "initial" not in graph:
        raise ValueError("Graph does not define 'initial'.")

    if "states" not in graph:
        raise ValueError("Graph does not define 'states'.")

    if not isinstance(graph["states"], dict):
        raise ValueError("'states' must be an object.")

    if graph["initial"] not in graph["states"]:
        raise ValueError(
            f"Initial state '{graph['initial']}' "
            "does not exist in 'states'."
        )


def build_output_path(
    output_dir: Path | None,
) -> Path:
    target_dir = output_dir or Path(__file__).parent / "diagrams"
    target_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime(TIMESTAMP_FORMAT)

    return target_dir / f"{OUTPUT_PREFIX}-{timestamp}.md"


# ============================================================
# Mermaid normalization
# ============================================================

def normalize_text(value: str) -> str:
    value = str(value)

    value = value.replace("\r", " ")
    value = value.replace("\n", " ")

    value = re.sub(r"\s+", " ", value)

    return value.strip()


def normalize_event(event: str) -> str:
    return normalize_text(event)


def normalize_condition(condition: str) -> str:
    return normalize_text(condition)


def build_label(
    event: str,
    condition: str | None = None,
) -> str:
    event = normalize_event(event)

    if not condition:
        return event

    condition = normalize_condition(condition)

    return f"{event}<br/>{condition}"


# ============================================================
# Transition handling
# ============================================================

def should_hide_transition(
    event: str,
    transition: dict,
) -> bool:
    if event in HIDDEN_EVENTS:
        return True

    target = transition.get("target")

    if HIDE_ABORT_TRANSITIONS and target == "abort":
        return True

    return False


def build_standard_transitions(
    state_name: str,
    state_definition: dict,
) -> list[str]:
    lines = []

    transitions = state_definition.get("on", {})

    for event, transition in transitions.items():
        if not isinstance(transition, dict):
            continue

        if should_hide_transition(event, transition):
            continue

        target = transition.get("target")

        if not target:
            continue

        condition = transition.get("condition")

        label = build_label(
            event=event,
            condition=condition,
        )

        lines.append(
            f"    {state_name} --> {target}: {label}"
        )

    return lines


def build_switch_transitions(
    state_name: str,
    state_definition: dict,
) -> list[str]:
    lines = []

    transitions = state_definition.get("on", {})

    for switch_value, transition in transitions.items():
        if not isinstance(transition, dict):
            continue

        if should_hide_transition(switch_value, transition):
            continue

        target = transition.get("target")

        if not target:
            continue

        label = normalize_text(switch_value)

        lines.append(
            f"    {state_name} --> {target}: {label}"
        )

    return lines


# ============================================================
# State classification
# ============================================================

def get_script_states(states: dict) -> list[str]:
    return [
        state_name
        for state_name, definition in states.items()
        if "scripts" in definition
    ]


def get_switch_states(states: dict) -> list[str]:
    return [
        state_name
        for state_name, definition in states.items()
        if "switch" in definition
    ]


def get_final_states(states: dict) -> list[str]:
    return [
        state_name
        for state_name, definition in states.items()
        if definition.get("type") == "final"
    ]


# ============================================================
# Mermaid generation
# ============================================================

def graph_to_mermaid(graph: dict) -> str:
    states = graph["states"]
    initial = graph["initial"]

    lines = [
        "stateDiagram-v2",
        "",
        f"    [*] --> {initial}",
        "",
    ]

    for state_name, state_definition in states.items():
        if state_definition.get("type") == "final":
            continue

        if "switch" in state_definition:
            transition_lines = build_switch_transitions(
                state_name,
                state_definition,
            )
        else:
            transition_lines = build_standard_transitions(
                state_name,
                state_definition,
            )

        if transition_lines:
            lines.extend(transition_lines)
            lines.append("")

    final_states = get_final_states(states)

    for state_name in final_states:
        lines.append(f"    {state_name} --> [*]")

    if final_states:
        lines.append("")

    script_states = get_script_states(states)
    switch_states = get_switch_states(states)

    lines.append(
        f"    classDef scriptState {SCRIPT_STATE_STYLE}"
    )

    lines.append(
        f"    classDef switchState {SWITCH_STATE_STYLE}"
    )

    if script_states:
        lines.append("")
        lines.append(
            "    class "
            + ",".join(script_states)
            + " scriptState"
        )

    if switch_states:
        lines.append(
            "    class "
            + ",".join(switch_states)
            + " switchState"
        )

    return "\n".join(lines).rstrip()


def build_markdown(graph: dict) -> str:
    graph_id = graph.get("id", "graph")
    version = graph.get("version")

    title = f"# {graph_id}"

    if version:
        title += f" v{version}"

    mermaid = graph_to_mermaid(graph)

    return (
        f"{title}\n\n"
        "```mermaid\n"
        f"{mermaid}\n"
        "```\n"
    )


# ============================================================
# Main
# ============================================================

def main():
    args = parse_args()

    input_path = args.input.resolve()

    graph = load_graph(input_path)

    output_path = build_output_path(
        output_dir=args.output_dir,
    )

    markdown = build_markdown(graph)

    output_path.write_text(
        markdown,
        encoding="utf-8",
    )

    print(output_path)


if __name__ == "__main__":
    main()