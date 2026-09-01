#!/usr/bin/env python3

import argparse
import re
import sys
from pathlib import Path


IDENTIFIER_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
GROUP_PATTERN = re.compile(r"^\([a-z0-9]+(?:-[a-z0-9]+)*\)$")
LOCAL_JOBS_RELATIVE_PATH = Path(".graph-engineering/local/jobs")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Resolve a tentative local job path without modifying the project."
    )
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--job-identifier", required=True)
    parser.add_argument("--job-path", default=None)
    return parser.parse_args()


def validate_identifier(value: str) -> str:
    if not IDENTIFIER_PATTERN.fullmatch(value):
        raise ValueError(f"job-identifier must be kebab-case: {value}")
    return value


def parse_job_path(value: str | None, identifier: str) -> tuple[str, ...]:
    normalized_path = value if value is not None else f"/{identifier}"
    if not normalized_path.startswith("/") or normalized_path.startswith("//"):
        raise ValueError("job-path must start with exactly one slash")
    if normalized_path.endswith("/") or "\\" in normalized_path:
        raise ValueError("job-path must not end with a slash or use backslashes")

    parts = tuple(normalized_path[1:].split("/"))
    if not parts or any(part in {"", ".", ".."} for part in parts):
        raise ValueError("job-path contains an invalid path segment")
    if parts[-1] != identifier:
        raise ValueError("the final job-path segment must equal job-identifier")
    if any(not GROUP_PATTERN.fullmatch(part) for part in parts[:-1]):
        raise ValueError("every job group must be a parenthesized kebab-case segment")
    return parts


def ensure_within(path: Path, root: Path):
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise ValueError("job-path escapes the local jobs root") from exc


def resolve_local_job_path(
    project_root: Path,
    job_identifier: str,
    job_path: str | None = None,
) -> Path:
    if not project_root.is_absolute():
        raise ValueError("project-root must be an absolute path")
    resolved_project_root = project_root.resolve()
    if not resolved_project_root.is_dir():
        raise ValueError("project-root must identify an existing directory")

    identifier = validate_identifier(job_identifier)
    parts = parse_job_path(job_path, identifier)
    jobs_root = (resolved_project_root / LOCAL_JOBS_RELATIVE_PATH).resolve()
    resolved_job_path = jobs_root.joinpath(*parts).resolve()
    ensure_within(resolved_job_path, jobs_root)
    return resolved_job_path


def main() -> int:
    args = parse_args()
    try:
        resolved_job_path = resolve_local_job_path(
            project_root=args.project_root,
            job_identifier=args.job_identifier,
            job_path=args.job_path,
        )
    except (OSError, ValueError) as exc:
        print(f"resolve_local_job_path: {exc}", file=sys.stderr)
        return 1

    print(resolved_job_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
