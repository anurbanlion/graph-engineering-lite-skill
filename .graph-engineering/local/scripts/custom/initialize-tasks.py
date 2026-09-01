#!/usr/bin/env python3
"""Initialize empty manage-tasks outputs for initiatives without a task list."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path


INITIATIVE_HEADING_PATTERN = re.compile(r"^##\s+(?P<domain>\S.*?)\s*$")
TASK_LIST_LINK_PATTERN = re.compile(
    r"^\s*-\s+\[Task list\]\([^)]+\)\s*$", re.IGNORECASE
)


def parse_initiative_sections(document: Path) -> list[tuple[str, list[str]]]:
    """Return the domain and content lines for every initiative section."""
    initiatives: list[tuple[str, list[str]]] = []
    domain: str | None = None
    section_lines: list[str] = []

    for line in document.read_text(encoding="utf-8").splitlines():
        match = INITIATIVE_HEADING_PATTERN.match(line)
        if match:
            if domain is not None:
                initiatives.append((domain, section_lines))
            domain = match.group("domain")
            section_lines = []
        elif domain is not None:
            section_lines.append(line)

    if domain is not None:
        initiatives.append((domain, section_lines))

    return initiatives


def has_task_list(section_lines: list[str]) -> bool:
    """Return whether an initiative section already links to a task list."""
    return any(TASK_LIST_LINK_PATTERN.match(line) for line in section_lines)


def resolve_output_path(domain: str, resolver: Path) -> Path:
    """Resolve a new manage-tasks output path through the shared resolver."""
    completed = subprocess.run(
        [sys.executable, str(resolver), domain, "manage-tasks"],
        check=True,
        capture_output=True,
        text=True,
    )
    output_path = completed.stdout.strip()

    if not output_path:
        raise RuntimeError(
            f"resolve_output_path.py returned no output path for domain '{domain}'."
        )

    return Path(output_path)


def initialize_task_lists(document: Path, resolver: Path) -> None:
    """Create empty task-list outputs for initiatives that have none."""
    for domain, section_lines in parse_initiative_sections(document):
        if has_task_list(section_lines):
            continue

        output_path = resolve_output_path(domain, resolver)
        output_path.touch(exist_ok=False)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Create empty manage-tasks outputs for initiatives without a Task list "
            "link in a compiled global initiative document."
        )
    )
    parser.add_argument(
        "document",
        type=Path,
        help="Path to the compiled global initiative Markdown document.",
    )
    arguments = parser.parse_args()

    document = arguments.document.resolve()
    if not document.is_file():
        parser.error(f"Document not found: {document}")

    resolver = Path(__file__).resolve().parents[1] / "resolve_output_path.py"
    initialize_task_lists(document, resolver)


if __name__ == "__main__":
    main()
