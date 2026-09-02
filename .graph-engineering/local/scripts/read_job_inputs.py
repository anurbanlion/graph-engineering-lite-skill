#!/usr/bin/env python3

import sys

from lib.errors import fail
from lib.paths import get_project_root
from lib.resolve_job import JobResolutionError, resolve_job
from lib.sections import extract_section


def main():
    if len(sys.argv) < 2:
        fail("Usage: python3 read_job_inputs.py <job-name>")

    job_name = sys.argv[1]

    project_root = get_project_root()

    try:
        resolved_job = resolve_job(job_name, project_root)
    except JobResolutionError as error:
        fail(str(error))
    job_md_path = resolved_job.job_md_path

    if not job_md_path:
        fail(f"Job not found: {job_name}")

    try:
        content = job_md_path.read_text(encoding="utf-8")
    except Exception as e:
        fail(f"Error reading {job_md_path}: {e}")

    inputs = extract_section(content, "## Inputs")

    print(f"===== JOB INPUTS: {job_name} =====")
    if inputs:
        print(inputs)
    else:
        print("No inputs required.")
    print(f"===== END JOB INPUTS: {job_name} =====")


if __name__ == "__main__":
    main()
