#!/usr/bin/env python3

import re
import sys

from lib.errors import fail
from lib.paths import get_project_root


def validate_name(value: str, label: str) -> None:
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", value):
        fail(f"{label} MUST be a non-empty kebab-case identifier.")


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        fail("Usage: python3 resolve_latest_output_path.py <domain> <job-name>")

    domain = argv[1]
    job_name = argv[2]
    if not domain:
        return 2

    validate_name(domain, "domain")
    validate_name(job_name, "job-name")

    project_root = get_project_root()
    output_dir = project_root / ".graph-engineering" / "runs" / domain / job_name
    if not output_dir.is_dir():
        fail(f'No outputs found for domain "{domain}" and job "{job_name}".')

    output_files = sorted(
        (
            path
            for path in output_dir.iterdir()
            if path.is_file()
            and path.name.startswith("OUTPUT-")
            and path.suffix == ".md"
        ),
        key=lambda path: path.name,
        reverse=True,
    )
    if not output_files:
        fail(f'No output files found for domain "{domain}" and job "{job_name}".')

    print(str(output_files[0].resolve()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
