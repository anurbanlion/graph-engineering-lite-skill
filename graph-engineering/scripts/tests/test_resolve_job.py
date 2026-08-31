from pathlib import Path

import pytest

from lib.resolve_job import JobResolutionError, resolve_job


def create_job(
    directory: Path,
    *,
    with_job_md: bool = True,
    with_graph_json: bool = False,
    with_scripts: bool = False,
) -> Path:
    directory.mkdir(parents=True)
    if with_job_md:
        (directory / "JOB.md").write_text("definition\n", encoding="utf-8")
    if with_graph_json:
        (directory / "GRAPH.json").write_text("{}\n", encoding="utf-8")
    if with_scripts:
        (directory / "scripts").mkdir()
    return directory.resolve()


def local_job_path(project_root: Path, job_identifier: str) -> Path:
    return project_root / ".graph-engineering" / "local" / "jobs" / job_identifier


def skill_job_path(skill_root: Path, *parts: str) -> Path:
    return skill_root.joinpath("jobs", *parts)


# Rule: Validate job identifier


def test_identifier_is_valid(tmp_path):
    project_root = tmp_path / "project"
    skill_root = tmp_path / "skill"
    expected_path = create_job(local_job_path(project_root, "my-job"))

    resolved = resolve_job("my-job", project_root, skill_root)

    assert resolved.job_folder_path == expected_path


@pytest.mark.parametrize(
    "job_identifier",
    [
        "",
        "group/design",
        "group\\design",
        ".",
        "..",
        "Design-Job",
        "design_job",
        "design job",
        "design--job",
    ],
)
def test_identifier_is_invalid(tmp_path, job_identifier):
    with pytest.raises(JobResolutionError):
        resolve_job(job_identifier, tmp_path / "project", tmp_path / "skill")


# Rule: Discover local job


def test_local_job_exists_exactly(tmp_path):
    project_root = tmp_path / "project"
    skill_root = tmp_path / "skill"
    expected_path = create_job(local_job_path(project_root, "my-job"))

    resolved = resolve_job("my-job", project_root, skill_root)

    assert resolved.job_folder_path == expected_path
    assert resolved.source == "local"


def test_local_job_does_not_exist(tmp_path):
    project_root = tmp_path / "project"
    skill_root = tmp_path / "skill"
    expected_path = create_job(skill_job_path(skill_root, "my-job"))

    resolved = resolve_job("my-job", project_root, skill_root)

    assert resolved.job_folder_path == expected_path
    assert resolved.source == "skill"


# Rule: Discover skill jobs


@pytest.mark.parametrize(
    "skill_relative_path",
    [
        ("my-job",),
        ("(authoring)", "my-job"),
        ("(workflow)", "(testing)", "my-job"),
    ],
)
def test_exactly_one_skill_job_exists(tmp_path, skill_relative_path):
    project_root = tmp_path / "project"
    skill_root = tmp_path / "skill"
    expected_path = create_job(skill_job_path(skill_root, *skill_relative_path))

    resolved = resolve_job("my-job", project_root, skill_root)

    assert resolved.job_folder_path == expected_path
    assert resolved.source == "skill"


def test_no_skill_job_exists(tmp_path):
    with pytest.raises(JobResolutionError, match="not found"):
        resolve_job("my-job", tmp_path / "project", tmp_path / "skill")


def test_two_or_more_skill_jobs_exist(tmp_path):
    project_root = tmp_path / "project"
    skill_root = tmp_path / "skill"
    create_job(skill_job_path(skill_root, "my-job"))
    create_job(skill_job_path(skill_root, "(authoring)", "my-job"))

    with pytest.raises(JobResolutionError, match="ambiguous") as error:
        resolve_job("my-job", project_root, skill_root)

    assert "my-job" in str(error.value)


# Rule: Validate job definition


def test_candidate_job_folder_path_with_job_md_is_valid(tmp_path):
    project_root = tmp_path / "project"
    skill_root = tmp_path / "skill"
    expected_path = create_job(local_job_path(project_root, "my-job"))

    resolved = resolve_job("my-job", project_root, skill_root)

    assert resolved.job_folder_path == expected_path
    assert resolved.job_md_path == expected_path / "JOB.md"


@pytest.mark.parametrize("candidate_source", ["local", "skill"])
def test_candidate_job_folder_path_without_job_md_is_invalid(
    tmp_path,
    candidate_source,
):
    project_root = tmp_path / "project"
    skill_root = tmp_path / "skill"
    candidate_path = (
        local_job_path(project_root, "my-job")
        if candidate_source == "local"
        else skill_job_path(skill_root, "my-job")
    )
    create_job(candidate_path, with_job_md=False, with_graph_json=True)

    with pytest.raises(JobResolutionError, match="JOB.md"):
        resolve_job("my-job", project_root, skill_root)


# Rule: Prioritize local job


def test_valid_local_job_and_no_skill_job_returns_local(tmp_path):
    project_root = tmp_path / "project"
    skill_root = tmp_path / "skill"
    expected_path = create_job(local_job_path(project_root, "my-job"))

    resolved = resolve_job("my-job", project_root, skill_root)

    assert resolved.job_folder_path == expected_path
    assert resolved.source == "local"


def test_valid_skill_job_and_no_local_job_returns_skill(tmp_path):
    project_root = tmp_path / "project"
    skill_root = tmp_path / "skill"
    expected_path = create_job(skill_job_path(skill_root, "(authoring)", "my-job"))

    resolved = resolve_job("my-job", project_root, skill_root)

    assert resolved.job_folder_path == expected_path
    assert resolved.source == "skill"


def test_valid_local_and_skill_jobs_return_local(tmp_path):
    project_root = tmp_path / "project"
    skill_root = tmp_path / "skill"
    local_path = create_job(local_job_path(project_root, "my-job"))
    create_job(skill_job_path(skill_root, "(authoring)", "my-job"))

    resolved = resolve_job("my-job", project_root, skill_root)

    assert resolved.job_folder_path == local_path
    assert resolved.source == "local"


def test_invalid_local_candidate_and_valid_skill_job_fails_without_fallback(tmp_path):
    project_root = tmp_path / "project"
    skill_root = tmp_path / "skill"
    create_job(local_job_path(project_root, "my-job"), with_job_md=False)
    create_job(skill_job_path(skill_root, "(authoring)", "my-job"))

    with pytest.raises(JobResolutionError, match="JOB.md"):
        resolve_job("my-job", project_root, skill_root)


# Rule: Resolve job


def test_a_job_is_resolved_with_the_documented_result_fields(tmp_path):
    project_root = tmp_path / "project"
    skill_root = tmp_path / "skill"
    job_path = create_job(
        local_job_path(project_root, "my-job"),
        with_graph_json=True,
        with_scripts=True,
    )

    resolved = resolve_job("my-job", project_root, skill_root)

    assert resolved.identifier == "my-job"
    assert resolved.job_folder_path == job_path
    assert resolved.source == "local"
    assert resolved.job_md_path == job_path / "JOB.md"
    assert resolved.graph_json_path == job_path / "GRAPH.json"
    assert resolved.scripts_folder_path == job_path / "scripts"


def test_no_job_is_resolved(tmp_path):
    with pytest.raises(JobResolutionError, match="not found"):
        resolve_job("my-job", tmp_path / "project", tmp_path / "skill")


