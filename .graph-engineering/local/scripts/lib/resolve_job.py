from dataclasses import dataclass
from pathlib import Path
from typing import Literal
import re


LOCAL_JOBS_RELATIVE_PATH = Path(".graph-engineering/local/jobs")
JOB_NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class JobResolutionError(ValueError):
    """Report an invalid, missing, or ambiguous job resolution."""


@dataclass(frozen=True)
class ResolvedJob:
    """Describe the selected job and its optional resources."""

    identifier: str
    job_folder_path: Path
    source: Literal["local", "skill"]

    @property
    def job_md_path(self) -> Path:
        """Return the required JOB.md path for this valid resolved job."""
        return self.job_folder_path / "JOB.md"

    @property
    def graph_json_path(self) -> Path | None:
        """Return GRAPH.json when the resolved job provides one."""
        path = self.job_folder_path / "GRAPH.json"
        return path if path.is_file() else None

    @property
    def scripts_folder_path(self) -> Path | None:
        """Return scripts/ when the resolved job provides one."""
        path = self.job_folder_path / "scripts"
        return path if path.is_dir() else None



def get_skill_root() -> Path:
    """Resolve graph-engineering/ from scripts/lib/resolve_job.py."""
    return Path(__file__).resolve().parents[2]


def is_job_folder(path: Path) -> bool:
    """Return whether a job folder provides its required JOB.md definition."""
    return path.is_dir() and (path / "JOB.md").is_file()


def validate_job_identifier(job_name: str) -> None:
    """Require one logical directory name without path traversal."""
    if (
        not job_name
        or Path(job_name).name != job_name
        or "/" in job_name
        or "\\" in job_name
        or job_name in {".", ".."}
    ):
        raise JobResolutionError(
            f'Invalid job identifier "{job_name}"; expected one directory name.'
        )


def validate_job_format(job_name: str) -> None:
    """Require the logical job identifier to use kebab-case."""
    if not JOB_NAME_PATTERN.fullmatch(job_name):
        raise JobResolutionError(
            f'Invalid job format "{job_name}"; expected kebab-case.'
        )


def validate_job_definition(
    job_folder_path: Path,
    source: Literal["local", "skill"],
    job_name: str,
) -> None:
    """Require a discovered candidate folder to contain JOB.md."""
    if not is_job_folder(job_folder_path):
        raise JobResolutionError(
            f'{source.capitalize()} job "{job_name}" has no JOB.md: '
            f"{job_folder_path}"
        )


def find_skill_job_folder_paths(
    skill_jobs_root: Path,
    job_name: str,
) -> list[Path]:
    """Find every job-named folder below skill_root/jobs, before validation."""
    if not skill_jobs_root.is_dir():
        return []

    return sorted(
        (
            path.resolve()
            for path in skill_jobs_root.rglob(job_name)
            if path.name == job_name and path.is_dir()
        ),
        key=str,
    )


def find_global_job_directories(
    global_jobs_root: Path,
    job_name: str,
) -> list[Path]:
    """Provide the previous discovery helper name during the transition."""
    return find_skill_job_folder_paths(global_jobs_root, job_name)


def resolve_job(
    job_name: str,
    project_root: Path,
    skill_root: Path | None = None,
) -> ResolvedJob:
    """Resolve a valid flat local job before one unique skill job."""
    validate_job_identifier(job_name)
    validate_job_format(job_name)

    resolved_project_root = Path(project_root).resolve()
    resolved_skill_root = (
        Path(skill_root).resolve()
        if skill_root is not None
        else get_skill_root()
    )

    local_job_folder_path = (
        resolved_project_root / LOCAL_JOBS_RELATIVE_PATH / job_name
    )
    if is_job_folder(local_job_folder_path):
        resolved_local_job_folder_path = local_job_folder_path.resolve()
        validate_job_definition(
            resolved_local_job_folder_path,
            "local",
            job_name,
        )
        return ResolvedJob(
            identifier=job_name,
            job_folder_path=resolved_local_job_folder_path,
            source="local",
        )

    skill_jobs_root = resolved_skill_root / "jobs"
    skill_matches = find_skill_job_folder_paths(skill_jobs_root, job_name)

    if not skill_matches:
        raise JobResolutionError(f'Job "{job_name}" not found.')

    if len(skill_matches) > 1:
        formatted_matches = "\n".join(f"- {path}" for path in skill_matches)
        raise JobResolutionError(
            f'Job "{job_name}" is ambiguous:\n{formatted_matches}'
        )

    skill_job_folder_path = skill_matches[0]
    validate_job_definition(skill_job_folder_path, "skill", job_name)
    return ResolvedJob(
        identifier=job_name,
        job_folder_path=skill_job_folder_path,
        source="skill",
    )


