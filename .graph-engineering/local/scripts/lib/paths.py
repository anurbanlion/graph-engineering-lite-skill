import os
from pathlib import Path

from .errors import fail

# ---------------------------------------------------------------------
# Path constants
# ---------------------------------------------------------------------

AGENT_SKILL_FOLDER = Path(
    os.environ.get("CODEX_AGENT_SKILL_FOLDER", ".codex/skills")
)

SKILL_LOCATION = AGENT_SKILL_FOLDER / "graph-engineering"

RUNTIME_RELATIVE_PATH = Path(".graph-engineering/runtime")

JOBS_RELATIVE_PATH = SKILL_LOCATION / "jobs"

# ---------------------------------------------------------------------
# Project root
# ---------------------------------------------------------------------


def get_project_root():
    """Resolve and validate the project root from the current working directory."""
    project_root = Path.cwd().resolve()
    # Simple validation that we are in the project root
    if not (project_root / ".codex").is_dir():
        fail("Unable to locate .codex directory. Must be run from project root.")
    return project_root


# ---------------------------------------------------------------------
# Jobs directory
# ---------------------------------------------------------------------


def get_jobs_dir(project_root):
    """Return the absolute path to the jobs directory."""
    return project_root / JOBS_RELATIVE_PATH


# ---------------------------------------------------------------------
# Job file resolution
# ---------------------------------------------------------------------

def find_job_dir(jobs_dir, job_name):
    """Find the directory for the given job logical identifier."""
    for path in jobs_dir.rglob(job_name):
        if path.is_dir() and path.name == job_name:
            return path
    return None

def find_job_md(jobs_dir, job_name):
    """Find the JOB.md file for the given job logical identifier."""
    job_dir = find_job_dir(jobs_dir, job_name)
    if job_dir:
        job_md = job_dir / "JOB.md"
        if job_md.is_file():
            return job_md
    return None
