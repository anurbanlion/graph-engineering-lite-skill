#!/usr/bin/env python3

import argparse
import json
import re
from pathlib import Path


OUTPUT_FILENAME = "GRAPH.md"
SCRIPT_STATE_STYLE = "fill:#DCEBFF,stroke:#2563EB,stroke-width:2px,color:#111827"
SWITCH_STATE_STYLE = "fill:#FEE2E2,stroke:#DC2626,stroke-width:2px,color:#111827"
SPAWN_STATE_STYLE = "fill:#FEF3C7,stroke:#D97706,stroke-width:2px,color:#111827"
CONTEXT_UPDATE_PATTERN = re.compile(
    r"--context\s+([A-Za-z_][A-Za-z0-9_]*)=([^\s]+)"
)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate a Mermaid Markdown diagram from a GRAPH.json file."
    )
    parser.add_argument("input", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser.parse_args()


def load_graph(path: Path) -> dict:
    if not path.is_file():
        raise FileNotFoundError(f"Graph file does not exist: {path}")

    with path.open("r", encoding="utf-8") as source:
        graph = json.load(source)

    validate_graph(graph)
    return graph


def validate_graph(graph: dict):
    if not isinstance(graph, dict):
        raise ValueError("Graph root must be a JSON object.")

    initial = graph.get("initial")
    states = graph.get("states")

    if not isinstance(initial, str) or not initial:
        raise ValueError("Graph must define a non-empty initial state.")

    if not isinstance(states, dict):
        raise ValueError("Graph states must be an object.")

    if initial not in states:
        raise ValueError(f"Initial state does not exist: {initial}")

    for state_name, definition in states.items():
        if not isinstance(definition, dict):
            raise ValueError(f"State must be an object: {state_name}")

        state_type = definition.get("type")
        if state_type not in {"instruction", "script", "switch", "spawn", "final"}:
            raise ValueError(
                f"State must define a valid type: {state_name}"
            )
        for event, transition in definition.get("on", {}).items():
            if not isinstance(transition, dict):
                raise ValueError(
                    f"Transition must be an object: {state_name}.{event}"
                )

            target = transition.get("target")
            if target and target not in states:
                raise ValueError(
                    f"Transition target does not exist: {state_name}.{event} -> {target}"
                )


def normalize(value) -> str:
    text = str(value).replace("\r", " ").replace("\n", " ")
    return re.sub(r"\s+", " ", text).strip()


def escape_mermaid_text(value) -> str:
    return (
        normalize(value)
        .replace("&", "and")
        .replace("<", "")
        .replace(">", "")
    )


def extract_context_updates(transition: dict) -> list[str]:
    instructions = transition.get("instructions", [])
    if not isinstance(instructions, list):
        return []

    updates = []
    for instruction in instructions:
        if not isinstance(instruction, str):
            continue
        updates.extend(
            f"{key}={value}"
            for key, value in CONTEXT_UPDATE_PATTERN.findall(instruction)
        )
    return updates


def should_hide(transition: dict) -> bool:
    return transition.get("target") == "abort"


def transition_lines(state_name: str, definition: dict) -> list[str]:
    lines = []
    is_switch = definition.get("type") == "switch"

    for event, transition in definition.get("on", {}).items():
        if not isinstance(transition, dict) or should_hide(transition):
            continue

        target = transition.get("target")
        if not target:
            continue

        label = normalize(event)
        condition = transition.get("condition")
        if condition and not is_switch:
            label += f"<br/>{normalize(condition)}"

        context_updates = extract_context_updates(transition)
        if context_updates:
            formatted_updates = ", ".join(
                escape_mermaid_text(update) for update in context_updates
            )
            label += f"<br/>Context: {formatted_updates}"

        lines.append(f"    {state_name} --> {target}: {label}")

    return lines


def graph_to_mermaid(graph: dict) -> str:
    states = graph["states"]
    lines = ["stateDiagram-v2", "", f"    [*] --> {graph['initial']}", ""]

    for state_name, definition in states.items():
        if definition.get("type") == "final":
            continue

        generated = transition_lines(state_name, definition)
        if generated:
            lines.extend(generated)
            lines.append("")

    final_states = [
        name for name, definition in states.items()
        if definition.get("type") == "final"
    ]
    for state_name in final_states:
        lines.append(f"    {state_name} --> [*]")

    if final_states:
        lines.append("")

    lines.append(f"    classDef scriptState {SCRIPT_STATE_STYLE}")
    lines.append(f"    classDef switchState {SWITCH_STATE_STYLE}")
    lines.append(f"    classDef spawnState {SPAWN_STATE_STYLE}")

    script_states = [
        name for name, definition in states.items()
        if definition.get("type") == "script"
    ]
    switch_states = [
        name for name, definition in states.items()
        if definition.get("type") == "switch"
    ]
    spawn_states = [
        name for name, definition in states.items()
        if definition.get("type") == "spawn"
    ]

    if script_states:
        lines.extend(["", "    class " + ",".join(script_states) + " scriptState"])
    if switch_states:
        lines.append("    class " + ",".join(switch_states) + " switchState")
    if spawn_states:
        lines.append("    class " + ",".join(spawn_states) + " spawnState")

    return "\n".join(lines).rstrip()


def build_markdown(graph: dict) -> str:
    title = f"# {graph.get('id', 'graph')}"
    if graph.get("version"):
        title += f" v{graph['version']}"
    return f"{title}\n\n```mermaid\n{graph_to_mermaid(graph)}\n```\n"


def main():
    args = parse_args()
    graph = load_graph(args.input.resolve())
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / OUTPUT_FILENAME
    output_path.write_text(build_markdown(graph), encoding="utf-8")
    print(output_path)


if __name__ == "__main__":
    main()
