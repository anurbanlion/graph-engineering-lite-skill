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

    # Search for the job directory
    job_dir = None
    for path in jobs_dir.rglob(job_name):
        if path.is_dir() and path.name == job_name:
            job_dir = path
            break

    if not job_dir:
        fail(f"Job not found: {job_name}")

    graph_path = job_dir / "GRAPH.json"
    job_md_path = job_dir / "JOB.md"

    # Sub-machine / Graph detection
    if graph_path.is_file():
        print(f"===== SUB-MACHINE DETECTED: {job_name} =====")
        try:
            rel_path = graph_path.relative_to(project_root)
        except ValueError:
            rel_path = graph_path
        print(f"Graph path: {rel_path}")
        print("This job is defined by a GRAPH.json file. It does not have a sequential markdown process.")
        print("You MUST invoke this job as a sub-machine.")
        print(f"===== END SUB-MACHINE: {job_name} =====")
        sys.exit(2)

    # Markdown Job detection
    if job_md_path.is_file():
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
        sys.exit(0)

    fail(f"Neither GRAPH.json nor JOB.md found in {job_dir}")


if __name__ == "__main__":
    main()
