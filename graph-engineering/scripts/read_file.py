#!/usr/bin/env python3

import sys
from pathlib import Path

from lib.errors import fail
from lib.paths import get_project_root


def resolve_file_path(project_root: Path, file_name: str) -> Path:
    """Resolve a project-relative file path without allowing path traversal."""
    path = (project_root / file_name).resolve()
    try:
        path.relative_to(project_root)
    except ValueError:
        fail(f"File path must stay within the project: {file_name}")
    return path


def main() -> None:
    if len(sys.argv) != 2:
        fail("Usage: python3 read_file.py <project-relative-file-path>")

    file_name = sys.argv[1]
    project_root = get_project_root()
    file_path = resolve_file_path(project_root, file_name)
    if not file_path.is_file():
        fail(f"File not found: {file_name}")

    try:
        content = file_path.read_text(encoding="utf-8")
    except OSError as exc:
        fail(f"Unable to read {file_name}: {exc}")

    print(f"===== FILE: {file_name} =====")
    print(content, end="" if content.endswith("\n") else "\n")
    print(f"===== END FILE: {file_name} =====")


if __name__ == "__main__":
    main()
