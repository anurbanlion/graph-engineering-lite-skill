#!/usr/bin/env python3

import sys

from lib.errors import fail
from lib.paths import get_project_root
from lib.resolve_job import JobResolutionError, resolve_job
from lib.sections import extract_section


def main():
    if len(sys.argv) < 2:
        fail("Usage: python3 read_job_process.py <job-name>")

    job_name = sys.argv[1]

    project_root = get_project_root()

    try:
        resolved_job = resolve_job(job_name, project_root)
    except JobResolutionError as error:
        fail(str(error))

    job_dir = resolved_job.job_folder_path
    graph_path = resolved_job.graph_json_path
    job_md_path = resolved_job.job_md_path

    # Sub-machine / Graph detection
    if graph_path is not None:
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
