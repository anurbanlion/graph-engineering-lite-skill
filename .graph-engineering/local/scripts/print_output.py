#!/usr/bin/env python3

import sys
from pathlib import Path

from lib.errors import fail
from lib.paths import get_project_root


def resolve_output_file(project_root: Path, value: str) -> Path:
    candidate = Path(value)
    output_file = (
        candidate.resolve()
        if candidate.is_absolute()
        else (project_root / candidate).resolve()
    )
    try:
        output_file.relative_to(project_root)
    except ValueError:
        fail(f"Output path must stay within the project: {value}")
    if not output_file.is_file():
        fail(f"Output file not found: {value}")
    return output_file


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        fail("Usage: python3 print_output.py <output-path>")

    project_root = get_project_root()
    output_file = resolve_output_file(project_root, argv[1])
    try:
        content = output_file.read_text(encoding="utf-8")
    except OSError as error:
        fail(f"Unable to read output file {output_file}: {error}")

    relative_path = output_file.relative_to(project_root)
    print(f"===== MANAGED OUTPUT: /{relative_path} =====")
    print(content, end="" if content.endswith("\n") else "\n")
    print("===== END MANAGED OUTPUT =====")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
