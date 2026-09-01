#!/usr/bin/env python3
"""Synchronize configured repository sources into configured destinations."""

from __future__ import annotations

import json
import os
import re
import shutil
import stat
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


SCRIPT_DIRECTORY = Path(__file__).resolve().parent
REPOSITORY_DIRECTORY = SCRIPT_DIRECTORY.parent
ENVIRONMENT_FILE = REPOSITORY_DIRECTORY / ".env"
ENVIRONMENT_KEY_PATTERN = re.compile(r"^[A-Z][A-Z0-9_]*$")


class SyncError(Exception):
    """Represents an expected synchronization failure."""


@dataclass(frozen=True)
class SourceEntry:
    path: str
    destination_name: str


@dataclass(frozen=True)
class Source:
    path: Path
    destination_name: str
    is_directory: bool


@dataclass(frozen=True)
class PlannedCopy:
    source: Source
    destination_root: Path
    destination_path: Path


def fail(message: str) -> None:
    raise SyncError(message)


def parse_environment_file(content: str) -> dict[str, str]:
    values: dict[str, str] = {}

    for index, raw_line in enumerate(content.splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        separator_index = line.find("=")
        if separator_index <= 0:
            fail(f"invalid .env entry on line {index}")

        key = line[:separator_index].strip()
        value = line[separator_index + 1 :].strip()

        if not ENVIRONMENT_KEY_PATTERN.fullmatch(key):
            fail(f"invalid .env key on line {index}: {key}")

        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"\"", "'"}:
            value = value[1:-1]

        values[key] = value

    return values


def parse_json_array(value: str, variable_name: str) -> list[Any]:
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError:
        fail(f"{variable_name} MUST be a path or a JSON array")

    if not isinstance(parsed, list) or not parsed:
        fail(f"{variable_name} JSON array MUST contain one or more entries")

    return parsed


def path_basename(value: str) -> str:
    return os.path.basename(value.rstrip("/"))


def parse_source_entry(entry: Any) -> SourceEntry:
    if isinstance(entry, str):
        path = entry.strip()
        if not path:
            fail("SYNC_SOURCE_PATH entries MUST be non-empty paths")
        return SourceEntry(path=path, destination_name=path_basename(path))

    if isinstance(entry, dict):
        path_value = entry.get("path")
        destination_name_value = entry.get("destinationName")
        path = path_value.strip() if isinstance(path_value, str) else ""
        destination_name = (
            destination_name_value.strip()
            if isinstance(destination_name_value, str)
            else path_basename(path)
        )

        if not path:
            fail("SYNC_SOURCE_PATH object entries MUST include a non-empty path")

        if not destination_name or "/" in destination_name or "\\" in destination_name:
            fail(
                "SYNC_SOURCE_PATH destinationName MUST be a single file or folder "
                f"name: {destination_name}"
            )

        return SourceEntry(path=path, destination_name=destination_name)

    fail("SYNC_SOURCE_PATH JSON array entries MUST be paths or objects with path and destinationName")


def parse_source_entries(value: str) -> list[SourceEntry]:
    entries = parse_json_array(value, "SYNC_SOURCE_PATH") if value.startswith("[") else [value]
    return [parse_source_entry(entry) for entry in entries]


def parse_destination_paths(value: str) -> list[str]:
    destinations = (
        parse_json_array(value, "SYNC_DESTINATION_PATH") if value.startswith("[") else [value]
    )
    if any(not isinstance(destination, str) or not destination.strip() for destination in destinations):
        fail("SYNC_DESTINATION_PATH entries MUST be non-empty paths")
    return [destination.strip() for destination in destinations]


def read_configuration() -> tuple[list[SourceEntry], list[str]]:
    try:
        content = ENVIRONMENT_FILE.read_text(encoding="utf-8")
    except FileNotFoundError:
        fail(
            f"configuration file not found: {ENVIRONMENT_FILE}. Copy .env.example to .env and configure it."
        )

    configuration = parse_environment_file(content)
    source_path_value = configuration.get("SYNC_SOURCE_PATH")
    destination_path_value = configuration.get("SYNC_DESTINATION_PATH")

    if not source_path_value:
        fail("SYNC_SOURCE_PATH MUST be set in .env")
    if not destination_path_value:
        fail("SYNC_DESTINATION_PATH MUST be set in .env")

    return parse_source_entries(source_path_value), parse_destination_paths(destination_path_value)


def resolve_path(value: str, base_directory: Path) -> Path:
    return Path(os.path.abspath(value if os.path.isabs(value) else base_directory / value))


def require_existing_path(path: Path, label: str) -> os.stat_result:
    try:
        return path.stat()
    except FileNotFoundError:
        fail(f"{label} does not exist: {path}")


def require_directory(path: Path, label: str) -> None:
    if not require_existing_path(path, label) or not path.is_dir():
        fail(f"{label} is not a directory: {path}")


def is_inside(parent_path: Path, child_path: Path) -> bool:
    try:
        relative_path = os.path.relpath(child_path, parent_path)
    except ValueError:
        return False

    return relative_path != "." and relative_path != ".." and not relative_path.startswith(f"..{os.sep}") and not os.path.isabs(relative_path)


def validate_distinct_paths(paths: list[Path], message: str) -> None:
    for index, path in enumerate(paths):
        for other_path in paths[index + 1 :]:
            if path == other_path or is_inside(path, other_path) or is_inside(other_path, path):
                fail(message)


def remove_destination(path: Path) -> None:
    if not path.exists() and not path.is_symlink():
        return
    if path.is_dir() and not path.is_symlink():
        shutil.rmtree(path)
    else:
        path.unlink()


def copy_source(source: Source, destination_path: Path) -> None:
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    if source.is_directory:
        shutil.copytree(source.path, destination_path, symlinks=True, copy_function=shutil.copy2)
    else:
        shutil.copy2(source.path, destination_path, follow_symlinks=False)


def synchronize() -> None:
    if len(sys.argv) > 1:
        fail("this script does not accept arguments; configure .env in the repository root")

    source_entries, destination_path_values = read_configuration()
    sources: list[Source] = []
    for source_entry in source_entries:
        source_path = resolve_path(source_entry.path, REPOSITORY_DIRECTORY)
        source_stat = require_existing_path(source_path, "source path")
        sources.append(
            Source(
                path=source_path,
                destination_name=source_entry.destination_name,
                is_directory=stat.S_ISDIR(source_stat.st_mode),
            )
        )

    validate_distinct_paths(
        [source.path for source in sources],
        "source paths MUST be distinct and MUST NOT contain one another",
    )

    destination_roots: list[Path] = []
    for destination_path_value in destination_path_values:
        if not os.path.isabs(destination_path_value):
            fail(f"SYNC_DESTINATION_PATH MUST be absolute: {destination_path_value}")
        destination_roots.append(resolve_path(destination_path_value, REPOSITORY_DIRECTORY))

    validate_distinct_paths(
        destination_roots,
        "destination paths MUST be distinct and MUST NOT contain one another",
    )

    planned_copies: list[PlannedCopy] = []
    planned_destination_paths: list[Path] = []
    for destination_root in destination_roots:
        for source in sources:
            destination_path = resolve_path(source.destination_name, destination_root)
            if not is_inside(destination_root, destination_path):
                fail(f"resolved destination MUST stay inside destination root: {destination_path}")

            for other_source in sources:
                if destination_path == other_source.path or is_inside(destination_path, other_source.path):
                    fail("destination path must not contain a source path")
                if is_inside(other_source.path, destination_path):
                    fail("destination path must not be inside a source path")

            planned_copies.append(
                PlannedCopy(
                    source=source,
                    destination_root=destination_root,
                    destination_path=destination_path,
                )
            )
            planned_destination_paths.append(destination_path)

    validate_distinct_paths(
        planned_destination_paths,
        "resolved destination paths MUST be distinct and MUST NOT contain one another",
    )

    for destination_root in destination_roots:
        destination_root.mkdir(parents=True, exist_ok=True)
        require_directory(destination_root, "destination root")

    for planned_copy in planned_copies:
        remove_destination(planned_copy.destination_path)
        copy_source(planned_copy.source, planned_copy.destination_path)

    print("Sources synchronized successfully.")
    for planned_copy in planned_copies:
        print(f"Source: {planned_copy.source.path}")
        print(f"Destination: {planned_copy.destination_path}")


def main() -> int:
    try:
        synchronize()
    except SyncError as error:
        print(f"sync-folder: {error}", file=sys.stderr)
        return 1
    except Exception as error:
        print(f"sync-folder: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
