#!/usr/bin/env python3

import re
import sys

from lib.errors import fail
from lib.paths import get_project_root


def validate_name(value, label):
    """Validate that the value is a non-empty kebab-case identifier."""
    if not value or not re.match(r"^[a-z0-9]+(?:-[a-z0-9]+)*$", value):
        fail(f"{label} MUST be a non-empty kebab-case identifier.")


def main():
    if len(sys.argv) < 3:
        fail("Usage: python3 dump_latest_output.py <domain> <job-name>")

    domain = sys.argv[1]
    job_name = sys.argv[2]

    validate_name(domain, "domain")
    validate_name(job_name, "job-name")

    project_root = get_project_root()
    output_dir = project_root / ".graph-engineering" / "runs" / domain / job_name

    if not output_dir.is_dir():
        fail(f'No outputs found for domain "{domain}" and job "{job_name}".')

    output_files = sorted(
        [f for f in output_dir.iterdir() if f.name.startswith("OUTPUT-") and f.name.endswith(".md")],
        key=lambda f: f.name,
        reverse=True,
    )

    if not output_files:
        fail(f'No output files found for domain "{domain}" and job "{job_name}".')

    latest_file = output_files[0]

    try:
        content = latest_file.read_text(encoding="utf-8")
    except Exception as e:
        fail(f"Error reading {latest_file}: {e}")

    print(f"===== LATEST MANAGED OUTPUT: {domain} / {job_name} (/{latest_file.relative_to(project_root)}) =====")
    print(content.strip())
    print("===== END LATEST MANAGED OUTPUT =====")


if __name__ == "__main__":
    main()
