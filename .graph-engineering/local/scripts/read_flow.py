#!/usr/bin/env python3

import sys

from lib.errors import fail
from lib.paths import find_job_md, get_jobs_dir, get_project_root
from lib.sections import extract_section


def main():
    if len(sys.argv) < 2:
        fail("Usage: python3 read_flow.py <flow-name>")

    flow_name = sys.argv[1]

    project_root = get_project_root()
    flows_dir = project_root / ".codex" / "skills" / "graph-engineering" / "graphs"
    
    if not flows_dir.exists():
        fail(f"Flows directory not found: {flows_dir}")

    flow_dir = None
    for path in flows_dir.rglob(flow_name):
        if path.is_dir() and path.name == flow_name:
            flow_dir = path
            break

    if not flow_dir:
        fail(f"Flow not found: {flow_name}")

    graph_path = flow_dir / "GRAPH.json"

    if graph_path.is_file():
        print(f"===== FLOW DEFINITION: {flow_name} =====")
        try:
            content = graph_path.read_text(encoding="utf-8")
            print(content)
        except Exception as e:
            fail(f"Error reading {graph_path}: {e}")
        print(f"===== END FLOW DEFINITION: {flow_name} =====")
        sys.exit(0)

    fail(f"GRAPH.json not found in {flow_dir}")

if __name__ == "__main__":
    main()
