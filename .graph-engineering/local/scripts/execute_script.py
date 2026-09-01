#!/usr/bin/env python3
"""Resolve and execute one Python Graph Engineering script for an agent."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from lib.resolve_script import ScriptResolutionError, resolve_script


def parse_arguments(argv: list[str]) -> tuple[argparse.Namespace, list[str]]:
    """Parse Execute Script options before an optional script-argument separator."""
    parser = argparse.ArgumentParser(
        description="Resolve and execute one Python Graph Engineering script.",
        usage=(
            "%(prog)s <script-identifier> --project-root <absolute-path> "
            "[-- <script-arguments>...]"
        ),
    )
    parser.add_argument("script_identifier")
    parser.add_argument("--project-root", required=True, type=Path)

    separator_index = argv.index("--") if "--" in argv else len(argv)
    arguments = parser.parse_args(argv[:separator_index])
    return arguments, argv[separator_index + 1 :]


def resolve_project_root(candidate: Path) -> Path:
    """Require the explicit Project Root to be an existing absolute directory."""
    if not candidate.is_absolute():
        raise ValueError("--project-root must be an absolute path.")

    project_root = candidate.resolve()
    if not project_root.is_dir():
        raise ValueError("--project-root must identify an existing directory.")
    return project_root


def execute_script(
    script_identifier: str,
    project_root: Path,
    script_arguments: list[str],
) -> int:
    """Resolve one script and return its natural process exit code."""
    resolved_script = resolve_script(script_identifier, project_root)
    completed_process = subprocess.run(
        [sys.executable, str(resolved_script.script_path), *script_arguments],
        cwd=project_root,
        check=False,
    )
    return completed_process.returncode


def main(argv: list[str]) -> int:
    """Run the requested script without creating runtime state or transitions."""
    arguments, script_arguments = parse_arguments(argv)
    try:
        project_root = resolve_project_root(arguments.project_root)
        return execute_script(
            arguments.script_identifier,
            project_root,
            script_arguments,
        )
    except (ScriptResolutionError, ValueError, OSError) as error:
        print(f"execute-script: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
