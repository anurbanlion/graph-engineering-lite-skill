import os
import pytest
from pathlib import Path

from lib.paths import find_job_md, get_jobs_dir, get_project_root


# ---------------------------------------------------------------
# find_job_md
# ---------------------------------------------------------------


class TestFindJobMd:
    def test_finds_job_in_flat_structure(self, tmp_path):
        job_dir = tmp_path / "my-job"
        job_dir.mkdir()
        job_file = job_dir / "JOB.md"
        job_file.write_text("# my-job")

        result = find_job_md(tmp_path, "my-job")
        assert result == job_file

    def test_finds_job_in_nested_group(self, tmp_path):
        group_dir = tmp_path / "some-group" / "nested-job"
        group_dir.mkdir(parents=True)
        job_file = group_dir / "JOB.md"
        job_file.write_text("# nested-job")

        result = find_job_md(tmp_path, "nested-job")
        assert result == job_file

    def test_returns_none_when_job_not_found(self, tmp_path):
        result = find_job_md(tmp_path, "nonexistent-job")
        assert result is None

    def test_returns_none_in_empty_directory(self, tmp_path):
        result = find_job_md(tmp_path, "any-job")
        assert result is None

    def test_matches_directory_name_not_file_content(self, tmp_path):
        job_dir = tmp_path / "alpha"
        job_dir.mkdir()
        job_file = job_dir / "JOB.md"
        job_file.write_text("# beta")  # content says beta, dir says alpha

        assert find_job_md(tmp_path, "alpha") == job_file
        assert find_job_md(tmp_path, "beta") is None

    def test_ignores_non_job_md_files(self, tmp_path):
        job_dir = tmp_path / "my-job"
        job_dir.mkdir()
        (job_dir / "README.md").write_text("not a job")

        result = find_job_md(tmp_path, "my-job")
        assert result is None


# ---------------------------------------------------------------
# get_jobs_dir
# ---------------------------------------------------------------


class TestGetJobsDir:
    def test_returns_path_relative_to_project_root(self, tmp_path):
        result = get_jobs_dir(tmp_path)
        assert result == tmp_path / ".codex" / "skills" / "graph-engineering" / "jobs"

    def test_respects_custom_skill_folder(self, tmp_path, monkeypatch):
        monkeypatch.setenv("CODEX_AGENT_SKILL_FOLDER", "custom/skills")

        # Need to reimport to pick up the env var change
        import importlib
        import lib.paths
        importlib.reload(lib.paths)

        from lib.paths import get_jobs_dir as reloaded_get_jobs_dir

        result = reloaded_get_jobs_dir(tmp_path)
        assert "custom" in str(result)
        assert "graph-engineering" in str(result)

        # Restore default
        monkeypatch.delenv("CODEX_AGENT_SKILL_FOLDER", raising=False)
        importlib.reload(lib.paths)


# ---------------------------------------------------------------
# get_project_root
# ---------------------------------------------------------------


class TestGetProjectRoot:
    def test_fails_when_framework_not_found(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)

        with pytest.raises(SystemExit) as exc_info:
            get_project_root()

        assert exc_info.value.code == 1
