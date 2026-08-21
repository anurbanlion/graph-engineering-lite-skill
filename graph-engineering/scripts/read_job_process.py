#!/usr/bin/env python3

import sys

from lib.errors import fail
from lib.paths import find_job_md, get_jobs_dir, get_project_root
from lib.sections import extract_section


def main():
    if len(sys.argv) < 2:
        fail("Usage: python3 read_job_process.py <job-name>")

    job_name = sys.argv[1]

    project_root = get_project_root()
    jobs_dir = get_jobs_dir(project_root)

    if not jobs_dir.exists():
        fail(f"Jobs directory not found: {jobs_dir}")

    job_md_path = find_job_md(jobs_dir, job_name)

    if not job_md_path:
        fail(f"Job not found: {job_name}")

    try:
        content = job_md_path.read_text(encoding="utf-8")
    except Exception as e:
        fail(f"Error reading {job_md_path}: {e}")

    process_section = extract_section(content, "## Process")

    print(f"===== JOB PROCESS: {job_name} =====")
    if process_section:
        print(process_section)
    else:
        print("No process defined.")
    print(f"===== END JOB PROCESS: {job_name} =====")


if __name__ == "__main__":
    main()
