#!/usr/bin/env python3
"""Validate a job identifier and report its graph location."""

import argparse
import json
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--job-identifier", required=True)
    parser.add_argument("--project-root", required=True, type=Path)
    args = parser.parse_args()

    scripts_root = (args.project_root / ".graph-engineering" / "local" / "scripts").resolve()
    sys.path.insert(0, str(scripts_root))
    from lib.resolve_job import JobResolutionError, resolve_job

    try:
        resolved = resolve_job(args.job_identifier, args.project_root)
    except JobResolutionError as error:
        print(f"check_graph: {error}", file=sys.stderr)
        return 1

    graph_path = resolved.graph_json_path
    if graph_path is None:
        print(f"Job '{args.job_identifier}' has no GRAPH.json.", file=sys.stderr)
        return 1

    print(json.dumps({
        "job_name": resolved.identifier,
        "job_path": str(resolved.job_folder_path),
        "graph_path": str(graph_path),
        "source": resolved.source,
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
