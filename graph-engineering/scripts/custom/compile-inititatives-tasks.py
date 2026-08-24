#!/usr/bin/env python3
"""Compile initiative milestones and the first pending tasks into Markdown."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import yaml


RUNS_DIRECTORY = Path(".graph-engineering/runs")
CHARTER_JOB_NAME = "create-initiative"
TASK_LIST_JOB_NAMES = ("add-tasks", "manage-tasks")
MAX_PENDING_TASKS_PER_INITIATIVE = 15
MILESTONE_YAML_FORMAT = """\
title: <milestone title>
done: false
short_description: <short description shown in the compiler>
description: |
  <long-form notes and ideas kept in the charter>
"""
MILESTONE_HEADING_PATTERN = re.compile(
    r"^(?P<level>#{2,3})\s+.*\b(?:hitos|milestones)\b", re.IGNORECASE
)
HEADING_PATTERN = re.compile(r"^(?P<level>#+)\s+")
TASK_PATTERN = re.compile(
    r"^(?P<indent>[ \t]*)-\s+\[(?P<status>[ xX])\]\s+.+\S\s*$"
)


def latest_managed_output(job_directory: Path) -> Path | None:
    """Return the latest timestamped Managed Output in a job directory."""
    outputs = sorted(job_directory.glob("OUTPUT-*.md"))
    return outputs[-1] if outputs else None


def latest_task_list(initiative_directory: Path) -> Path | None:
    """Return the newest task-list output from add-tasks or manage-tasks."""
    outputs = [
        output
        for job_name in TASK_LIST_JOB_NAMES
        if (output := latest_managed_output(initiative_directory / job_name))
    ]
    return max(outputs, key=lambda output: output.name) if outputs else None


def format_milestone_block(block: str) -> tuple[list[str], bool]:
    """Format a YAML milestone block or preserve its original text."""
    fallback = [line.strip() for line in block.splitlines() if line.strip()]
    try:
        parsed = yaml.safe_load(block)
    except yaml.YAMLError:
        return fallback, False

    entries = [parsed] if isinstance(parsed, dict) else parsed
    if not isinstance(entries, list) or not all(isinstance(entry, dict) for entry in entries):
        return fallback, False

    formatted: list[str] = []
    for number, entry in enumerate(entries, start=1):
        title = entry.get("title") or entry.get("titulo")
        short_description = (
            entry.get("short_description")
            or entry.get("descripcion_corta")
            or entry.get("summary")
        )
        if not isinstance(title, str) or not isinstance(short_description, str):
            return fallback, False
        checkbox = "x" if entry.get("done") is True else " "
        formatted.append(
            f"- [{checkbox}] **{number}. {title}**: {short_description}"
        )

    return formatted or fallback, bool(formatted)


def extract_project_path(charter: Path) -> Path | None:
    """Return an absolute project_path declared in the charter frontmatter."""
    lines = charter.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        return None

    try:
        closing_index = lines.index("---", 1)
        frontmatter = yaml.safe_load("\n".join(lines[1:closing_index]))
    except (ValueError, yaml.YAMLError):
        return None

    project_path = frontmatter.get("project_path") if isinstance(frontmatter, dict) else None
    if not isinstance(project_path, str):
        return None

    path = Path(project_path)
    return path if path.is_absolute() else None


def extract_milestones(charter: Path) -> tuple[list[str], bool]:
    """Extract and format the content below the Hitos/Milestones subheader."""
    lines = charter.read_text(encoding="utf-8").splitlines()
    milestone_lines: list[str] = []
    collecting = False
    milestone_level = 0

    for line in lines:
        milestone_heading = MILESTONE_HEADING_PATTERN.match(line)
        if milestone_heading:
            collecting = True
            milestone_level = len(milestone_heading.group("level"))
            continue

        heading = HEADING_PATTERN.match(line)
        if collecting and heading and len(heading.group("level")) <= milestone_level:
            break

        if collecting:
            milestone_lines.append(line)

    return format_milestone_block("\n".join(milestone_lines).strip())


def extract_pending_tasks(task_list: Path) -> list[str]:
    """Return the first 15 pending tasks, preserving every nesting level."""
    blocks: list[list[tuple[str, bool]]] = []
    current_block: list[tuple[str, bool]] = []

    for line in task_list.read_text(encoding="utf-8").splitlines():
        match = TASK_PATTERN.match(line)
        if match is None:
            continue

        task = (line, match.group("status") == " ")
        if not match.group("indent"):
            if current_block:
                blocks.append(current_block)
            current_block = [task]
        elif current_block:
            current_block.append(task)

    if current_block:
        blocks.append(current_block)

    output: list[str] = []
    pending_count = 0
    for block in blocks:
        if not any(is_pending for _, is_pending in block):
            continue

        selected_block: list[str] = []
        for line, is_pending in block:
            if is_pending and pending_count == MAX_PENDING_TASKS_PER_INITIATIVE:
                break
            selected_block.append(line)
            pending_count += is_pending

        if selected_block:
            if output:
                output.append("")
            output.extend(selected_block)
        if pending_count == MAX_PENDING_TASKS_PER_INITIATIVE:
            break

    return output


def compile_portfolio() -> str:
    """Build the Markdown portfolio view from hardcoded project locations."""
    if not RUNS_DIRECTORY.is_dir():
        raise FileNotFoundError(f"Runs directory not found: {RUNS_DIRECTORY}")

    initiatives: list[
        tuple[str, Path, Path | None, Path | None, list[str], bool, list[str]]
    ] = []

    for initiative_directory in sorted(RUNS_DIRECTORY.iterdir()):
        if not initiative_directory.is_dir():
            continue

        charter = latest_managed_output(initiative_directory / CHARTER_JOB_NAME)
        task_list = latest_task_list(initiative_directory)
        if charter is None:
            continue

        project_path = extract_project_path(charter)
        milestones, milestones_are_yaml = extract_milestones(charter)
        tasks = extract_pending_tasks(task_list) if task_list else []
        initiatives.append(
            (
                initiative_directory.name,
                charter,
                task_list,
                project_path,
                milestones,
                milestones_are_yaml,
                tasks,
            )
        )

    output = ["# Initiative Milestones and Pending Tasks", ""]

    for (
        domain,
        charter,
        task_list,
        project_path,
        milestones,
        milestones_are_yaml,
        tasks,
    ) in initiatives:
        output.append(f"## {domain}")
        output.append("")
        output.append(f"- [Charter]({charter.resolve().as_uri()})")
        if task_list:
            output.append(f"- [Task list]({task_list.resolve().as_uri()})")
        if project_path:
            output.append(
                f"- Project folder: [{project_path}]({project_path})"
            )
        output.append("")

        output.append("### Milestones")
        if milestones:
            if milestones_are_yaml:
                output.extend(milestones)
            else:
                output.extend(f"- {milestone}" for milestone in milestones)
        else:
            output.append("- No milestones found.")
        output.append("")

        output.append(f"### First {MAX_PENDING_TASKS_PER_INITIATIVE} Pending Tasks")
        if tasks:
            output.extend(tasks)
        else:
            output.append("- No pending tasks found.")
        output.append("")

    output.append("")
    return "\n".join(output)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compile initiative milestones and the first 15 pending tasks."
    )
    parser.add_argument("output", type=Path, help="Markdown file to write")
    arguments = parser.parse_args()

    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(compile_portfolio(), encoding="utf-8")


if __name__ == "__main__":
    main()