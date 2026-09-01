#!/usr/bin/env python3

from lib.paths import get_project_root

def find_flow_paths(flows_dir, directory=None):
    """
    Recursively find all flow directories (containing GRAPH.json)
    and return their paths relative to flows_dir.
    """
    if directory is None:
        directory = flows_dir

    results = []

    try:
        entries = sorted(directory.iterdir())
    except OSError:
        return results

    for entry in entries:
        if not entry.is_dir():
            continue

        if (entry / "GRAPH.json").exists():
            results.append(str(entry.relative_to(flows_dir)))
        else:
            results.extend(find_flow_paths(flows_dir, entry))

    return results

def main():
    project_root = get_project_root()
    flows_dir = project_root / ".codex" / "skills" / "graph-engineering" / "graphs"

    if not flows_dir.is_dir():
        print("No flows directory found.")
        return

    flows = find_flow_paths(flows_dir)

    if not flows:
        print("No flows available.")
        return

    for flow in flows:
        print(flow)

if __name__ == "__main__":
    main()
