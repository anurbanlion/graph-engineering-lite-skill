#!/usr/bin/env python3

from lib.errors import fail
from lib.paths import get_jobs_dir, get_project_root


def find_job_paths(jobs_dir, directory=None):
    """
    Recursively find all job directories (containing JOB.md)
    and return their paths relative to jobs_dir.
    """
    if directory is None:
        directory = jobs_dir

    results = []

    try:
        entries = sorted(directory.iterdir())
    except OSError:
        return results

    for entry in entries:
        if not entry.is_dir():
            continue

        if (entry / "JOB.md").exists():
            results.append(str(entry.relative_to(jobs_dir)))
        else:
            results.extend(find_job_paths(jobs_dir, entry))

    return results


def main():
    project_root = get_project_root()
    jobs_dir = get_jobs_dir(project_root)

    if not jobs_dir.is_dir():
        print("No jobs directory found.")
        return

    jobs = find_job_paths(jobs_dir)

    if not jobs:
        print("No jobs available.")
        return

    for job in jobs:
        print(job)


if __name__ == "__main__":
    main()
