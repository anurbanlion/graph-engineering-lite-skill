#!/usr/bin/env python3

import argparse
import json
import re
from pathlib import Path


HIDDEN_EVENTS = {"ERROR", "AMBIGUOUS"}
HIDE_ABORT_TRANSITIONS = True
OUTPUT_FILENAME = "GRAPH.md"
SCRIPT_STATE_STYLE = "fill:#DCEBFF,stroke:#2563EB,stroke-width:2px,color:#111827"
SWITCH_STATE_STYLE = "fill:#FEE2E2,stroke:#DC2626,stroke-width:2px,color:#111827"


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


def should_hide(event: str, transition: dict) -> bool:
    if event in HIDDEN_EVENTS:
        return True
    return HIDE_ABORT_TRANSITIONS and transition.get("target") == "abort"


def transition_lines(state_name: str, definition: dict) -> list[str]:
    lines = []
    is_switch = "switch" in definition

    for event, transition in definition.get("on", {}).items():
        if not isinstance(transition, dict) or should_hide(event, transition):
            continue

        target = transition.get("target")
        if not target:
            continue

        label = normalize(event)
        condition = transition.get("condition")
        if condition and not is_switch:
            label += f"<br/>{normalize(condition)}"

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

    script_states = [
        name for name, definition in states.items()
        if "scripts" in definition
    ]
    switch_states = [
        name for name, definition in states.items()
        if "switch" in definition
    ]

    if script_states:
        lines.extend(["", "    class " + ",".join(script_states) + " scriptState"])
    if switch_states:
        lines.append("    class " + ",".join(switch_states) + " switchState")

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
