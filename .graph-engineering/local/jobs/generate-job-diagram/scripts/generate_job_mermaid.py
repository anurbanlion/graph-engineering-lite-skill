#!/usr/bin/env python3
"""Generate a local Mermaid diagram for a resolved job graph."""

import argparse
import subprocess
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--job-identifier", required=True)
    parser.add_argument("--project-root", required=True, type=Path)
    args = parser.parse_args()
    args = parser.parse_args()

    scripts_root = (args.project_root / ".graph-engineering" / "local" / "scripts").resolve()
    sys.path.insert(0, str(scripts_root))
    from lib.resolve_job import JobResolutionError, get_skill_root, resolve_job
    from resolve_local_job_path import resolve_local_job_path

    try:
        resolved = resolve_job(args.job_identifier, args.project_root)
    except JobResolutionError as error:
        print(f"generate_job_mermaid: {error}", file=sys.stderr)
        return 1

    graph_path = resolved.graph_json_path
    if graph_path is None:
        print(f"Job '{args.job_identifier}' has no GRAPH.json.", file=sys.stderr)
        return 1

    if resolved.source == "local":
        local_output = resolved.job_folder_path
    else:
        skill_jobs_root = (get_skill_root() / "jobs").resolve()
        relative_job_path = "/" + "/".join(resolved.job_folder_path.relative_to(skill_jobs_root).parts)
        local_output = resolve_local_job_path(args.project_root, args.job_identifier, relative_job_path)
    local_output.mkdir(parents=True, exist_ok=True)
    converter = scripts_root / "graph_to_mermaid.py"
    command = [sys.executable, str(converter), str(graph_path), "--output-dir", str(local_output)]
    completed = subprocess.run(command, cwd=args.project_root)
    if completed.returncode != 0:
        return completed.returncode

    print(local_output / "GRAPH.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
