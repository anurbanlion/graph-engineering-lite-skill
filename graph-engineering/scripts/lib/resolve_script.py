"""Resolve Python scripts from the local or selected Graph Engineering skill."""

from dataclasses import dataclass
from pathlib import Path
from typing import Literal
import re


LOCAL_SHARED_SCRIPTS_RELATIVE_PATH = Path(".graph-engineering/local/scripts")
LOCAL_JOBS_RELATIVE_PATH = Path(".graph-engineering/local/jobs")
SCRIPT_NAME_PATTERN = re.compile(r"^[a-z][a-z0-9]*(?:_[a-z0-9]+)*$")


class ScriptResolutionError(ValueError):
    """Report an invalid, missing, or ambiguous script resolution."""


@dataclass(frozen=True)
class ResolvedScript:
    """Describe the selected Python script and the store that provided it."""

    identifier: str
    script_path: Path
    source: Literal["local", "skill"]
    scope: Literal["shared", "job"]


def get_skill_root() -> Path:
    """Resolve graph-engineering/ from scripts/lib/resolve_script.py."""
    return Path(__file__).resolve().parents[2]


def validate_script_identifier(script_name: str) -> None:
    """Require one snake_case Python module name without a path or extension."""
    if (
        not script_name
        or Path(script_name).name != script_name
        or "/" in script_name
        or "\\" in script_name
        or script_name in {".", ".."}
        or script_name.endswith(".py")
    ):
        raise ScriptResolutionError(
            f'Invalid script identifier "{script_name}"; expected one name without .py.'
        )
    if not SCRIPT_NAME_PATTERN.fullmatch(script_name):
        raise ScriptResolutionError(
            f'Invalid script format "{script_name}"; expected snake_case.'
        )


def find_python_scripts(root: Path, script_name: str) -> list[Path]:
    """Find eligible files named <script_name>.py below one script root."""
    if not root.is_dir():
        return []

    expected_name = f"{script_name}.py"
    return sorted(
        (
            path.resolve()
            for path in root.rglob(expected_name)
            if path.is_file() and "__pycache__" not in path.parts
        ),
        key=str,
    )


def find_local_scripts(
    project_root: Path,
    script_name: str,
) -> list[tuple[Path, Literal["shared", "job"]]]:
    """Find shared scripts and scripts in direct local job folders."""
    shared_root = project_root / LOCAL_SHARED_SCRIPTS_RELATIVE_PATH
    local_jobs_root = project_root / LOCAL_JOBS_RELATIVE_PATH
    matches: list[tuple[Path, Literal["shared", "job"]]] = [
        (path, "shared")
        for path in find_python_scripts(shared_root, script_name)
    ]
    if not local_jobs_root.is_dir():
        return matches

    for local_job_folder_path in local_jobs_root.iterdir():
        if not local_job_folder_path.is_dir():
            continue
        matches.extend(
            (path, "job")
            for path in find_python_scripts(
                local_job_folder_path / "scripts",
                script_name,
            )
        )
    return sorted(matches, key=lambda match: str(match[0]))


def find_skill_scripts(
    skill_root: Path,
    script_name: str,
) -> list[tuple[Path, Literal["shared", "job"]]]:
    """Find shared scripts and scripts embedded in skill job folders."""
    shared_root = skill_root / "scripts"
    skill_jobs_root = skill_root / "jobs"
    return [
        *((path, "shared") for path in find_python_scripts(shared_root, script_name)),
        *((path, "job") for path in find_python_scripts(skill_jobs_root, script_name)
          if "scripts" in path.relative_to(skill_jobs_root).parts),
    ]


def resolve_script(
    script_name: str,
    project_root: Path,
    skill_root: Path | None = None,
) -> ResolvedScript:
    """Resolve one unique local script before one unique skill script."""
    validate_script_identifier(script_name)

    resolved_project_root = Path(project_root).resolve()
    resolved_skill_root = (
        Path(skill_root).resolve()
        if skill_root is not None
        else get_skill_root()
    )

    local_matches = find_local_scripts(resolved_project_root, script_name)
    if local_matches:
        return _resolve_single_match(script_name, local_matches, "local")

    skill_matches = find_skill_scripts(resolved_skill_root, script_name)
    if skill_matches:
        return _resolve_single_match(script_name, skill_matches, "skill")

    raise ScriptResolutionError(f'Script "{script_name}" not found.')


def _resolve_single_match(
    script_name: str,
    matches: list[tuple[Path, Literal["shared", "job"]]],
    source: Literal["local", "skill"],
) -> ResolvedScript:
    """Return the unique match or report every conflicting script path."""
    if len(matches) > 1:
        formatted_matches = "\n".join(f"- {path}" for path, _ in matches)
        raise ScriptResolutionError(
            f'Script "{script_name}" is ambiguous in {source} scripts:\n'
            f"{formatted_matches}"
        )

    script_path, scope = matches[0]
    return ResolvedScript(
        identifier=script_name,
        script_path=script_path,
        source=source,
        scope=scope,
    )
