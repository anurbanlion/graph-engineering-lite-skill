import json
from pathlib import Path

import check_job
import execute


def create_graph_job(job_folder_path: Path) -> None:
    job_folder_path.mkdir(parents=True)
    (job_folder_path / "JOB.md").write_text("job\n", encoding="utf-8")
    (job_folder_path / "GRAPH.json").write_text(
        json.dumps(
            {
                "initial": "start",
                "states": {"start": {"type": "other"}},
            }
        ),
        encoding="utf-8",
    )


def test_resolve_and_load_job_graph_uses_resolve_job_from_project_root(
    tmp_path,
    monkeypatch,
):
    project_root = tmp_path / "project"
    create_graph_job(
        project_root
        / ".graph-engineering"
        / "local"
        / "jobs"
        / "my-job"
    )
    monkeypatch.setattr(execute, "PROJECT_ROOT", project_root)

    graph = execute.resolve_and_load_job_graph("my-job")

    assert graph["initial"] == "start"
    assert graph["states"] == {"start": {"type": "other"}}


def test_new_execution_accepts_initial_context():
    inputs = execute.parse_command_line_inputs(
        [
            "execute.py",
            "--job",
            "execute-job",
            "--context",
            "job_name=design-job",
            "--execution-mode",
            "echo",
        ]
    )

    assert inputs.execution_type == "new"
    assert inputs.execution_mode == "echo"
    assert inputs.initial_context == {"job_name": "design-job"}


def test_initial_snapshot_merges_default_and_supplied_context():
    graph = {
        "initial": "start",
        "states": {"start": {}},
        "context": {"job_name": ""},
    }

    snapshot = execute.create_initial_snapshot(
        graph,
        "execute-job",
        "default",
        initial_context={"job_name": "design-job"},
    )

    assert snapshot["context"] == {"job_name": "design-job"}


def test_check_job_returns_only_a_status_code(tmp_path, monkeypatch):
    project_root = tmp_path / "project"
    create_graph_job(
        project_root
        / ".graph-engineering"
        / "local"
        / "jobs"
        / "design-job"
    )
    monkeypatch.setattr(check_job, "get_project_root", lambda: project_root)

    assert check_job.main(["check_job.py", "design-job"]) == 0
    assert check_job.main(["check_job.py", "missing-job"]) == 1
    assert check_job.main(["check_job.py"]) == 1


def test_execute_job_graph_starts_with_silent_job_resolution():
    graph_path = (
        Path(__file__).resolve().parents[2] / "jobs" / "execute-job" / "GRAPH.json"
    )
    graph = json.loads(graph_path.read_text(encoding="utf-8"))

    assert graph["context_schema"] == {"job_name": "string"}
    assert graph["context"] == {"job_name": ""}
    assert graph["initial"] == "resolvingRequestedJob"
    assert graph["states"]["resolvingRequestedJob"] == {
        "scripts": ["scripts/check_job.py {context.job_name}"],
        "exit_codes": {"0": "DONE", "1": "ERROR"},
        "on": {
            "DONE": {
                "target": "readingJobInputs",
                "condition": "The requested job resolves uniquely",
            },
            "ERROR": {
                "target": "discoveringJobs",
                "condition": (
                    "No requested job was provided or it could not resolve uniquely"
                ),
            },
        },
    }
