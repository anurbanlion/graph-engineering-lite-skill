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

EXECUTE_JOB_GRAPH_RELATIVE_PATH = (
    SKILL_LOCATION / "jobs/execute-job/GRAPH.json"
)

RUNTIME_RELATIVE_PATH = Path(".graph-engineering/runtime")

JOBS_RELATIVE_PATH = SKILL_LOCATION / "jobs"

# ---------------------------------------------------------------------
# Project root
# ---------------------------------------------------------------------


def get_project_root():
    """Resolve and validate the project root from the current working directory."""
    project_root = Path.cwd().resolve()

    # Note: This validation should done againt SKILL.md and a more specific validation should be done against execute-job/GRAPH.json
    # once we change the api to execute --job <job-name>
    framework_path = project_root / EXECUTE_JOB_GRAPH_RELATIVE_PATH

    if not framework_path.is_file():
        fail(
            "Unable to locate Graph Engineering framework. "
            f"Expected file at: '{framework_path}'."
        )

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


def find_job_md(jobs_dir, job_name):
    """Find the JOB.md file for the given job logical identifier."""
    for path in jobs_dir.rglob("JOB.md"):
        if path.parent.name == job_name:
            return path
    return None
