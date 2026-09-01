import subprocess
from pathlib import Path


def test_read_job_output_with_managed_output(tmp_path, monkeypatch):
    # Setup mock job
    job_dir = tmp_path / ".codex" / "skills" / "graph-engineering" / "jobs" / "my-job"
    job_dir.mkdir(parents=True)
    job_file = job_dir / "JOB.md"
    job_file.write_text(
        "# My Job\n\n## Process\n\nstep 1\n\n## Output\n\nThe job MUST produce a Managed Output.\n"
    )

    # We need to run the script via subprocess to test it end-to-end
    script_path = Path(__file__).resolve().parent.parent / "scripts" / "read_job_output.py"

    monkeypatch.chdir(tmp_path)

    # Need a mock GRAPH.json to bypass project root validation
    graph_path = tmp_path / ".codex" / "skills" / "graph-engineering" / "jobs" / "execute-job"
    graph_path.mkdir(parents=True)
    (graph_path / "GRAPH.json").write_text("{}")

    result = subprocess.run(
        ["python3", str(script_path), "my-job"],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "The job MUST produce a Managed Output." in result.stdout
    assert "===== JOB OUTPUT: my-job =====" in result.stdout


def test_read_job_output_without_output_section(tmp_path, monkeypatch):
    job_dir = tmp_path / ".codex" / "skills" / "graph-engineering" / "jobs" / "no-out-job"
    job_dir.mkdir(parents=True)
    job_file = job_dir / "JOB.md"
    job_file.write_text("# No Out Job\n\n## Process\n\njust context\n")

    script_path = Path(__file__).resolve().parent.parent / "scripts" / "read_job_output.py"
    monkeypatch.chdir(tmp_path)
    graph_path = tmp_path / ".codex" / "skills" / "graph-engineering" / "jobs" / "execute-job"
    graph_path.mkdir(parents=True)
    (graph_path / "GRAPH.json").write_text("{}")

    result = subprocess.run(
        ["python3", str(script_path), "no-out-job"],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "No output defined." in result.stdout
