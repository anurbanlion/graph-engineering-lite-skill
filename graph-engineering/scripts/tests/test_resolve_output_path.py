import subprocess
from pathlib import Path


def test_resolve_output_path_validates_kebab_case(tmp_path, monkeypatch):
    script_path = Path(__file__).resolve().parent.parent / "scripts" / "resolve_output_path.py"

    result = subprocess.run(
        ["python3", str(script_path), "invalid_domain", "valid-job"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1
    assert "MUST be a non-empty kebab-case identifier" in result.stderr

    result = subprocess.run(
        ["python3", str(script_path), "valid-domain", "invalid_job"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1
    assert "MUST be a non-empty kebab-case identifier" in result.stderr


def test_resolve_output_path_creates_directory_and_returns_path(tmp_path, monkeypatch):
    script_path = Path(__file__).resolve().parent.parent / "scripts" / "resolve_output_path.py"
    
    monkeypatch.chdir(tmp_path)
    graph_path = tmp_path / ".codex" / "skills" / "graph-engineering" / "jobs" / "execute-job"
    graph_path.mkdir(parents=True)
    (graph_path / "GRAPH.json").write_text("{}")

    result = subprocess.run(
        ["python3", str(script_path), "global", "compile-initiatives"],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    
    output_path_str = result.stdout.strip()
    assert output_path_str != ""
    
    output_path = Path(output_path_str)
    assert output_path.name.startswith("OUTPUT-")
    assert output_path.name.endswith(".md")
    
    # Verify it created the nested folders
    assert output_path.parent.name == "compile-initiatives"
    assert output_path.parent.parent.name == "global"
    assert output_path.parent.parent.parent.name == "runs"
    assert output_path.parent.parent.parent.parent.name == ".graph-engineering"
    
    assert output_path.parent.exists()
