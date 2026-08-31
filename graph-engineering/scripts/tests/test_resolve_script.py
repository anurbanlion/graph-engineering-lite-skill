from pathlib import Path

import pytest

from lib.resolve_script import (
    ScriptResolutionError,
    find_local_scripts,
    find_skill_scripts,
    resolve_script,
    validate_script_identifier,
)


def create_file(path: Path, content: str = "print('ok')\n") -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path.resolve()


def local_shared_script_path(project_root: Path, *parts: str) -> Path:
    return project_root.joinpath(
        ".graph-engineering",
        "local",
        "scripts",
        *parts,
    )


def local_job_script_path(
    project_root: Path,
    job_identifier: str,
    *parts: str,
) -> Path:
    return project_root.joinpath(
        ".graph-engineering",
        "local",
        "jobs",
        job_identifier,
        "scripts",
        *parts,
    )


def skill_shared_script_path(skill_root: Path, *parts: str) -> Path:
    return skill_root.joinpath("scripts", *parts)


def skill_job_script_path(
    skill_root: Path,
    job_folder_parts: tuple[str, ...],
    *parts: str,
) -> Path:
    return skill_root.joinpath("jobs", *job_folder_parts, "scripts", *parts)


# Rule: Validate script identifier


@pytest.mark.parametrize(
    "script_identifier",
    ["prepare", "read_job_inputs", "compile_initiatives_tasks", "version2_task3"],
)
def test_identifier_is_valid(script_identifier):
    validate_script_identifier(script_identifier)


@pytest.mark.parametrize(
    "script_identifier",
    [
        "",
        "nested/prepare",
        "nested\\prepare",
        ".",
        "..",
        "prepare.py",
        "read-job-inputs",
        "ReadJobInputs",
        "read job inputs",
        "2read_inputs",
        "read__inputs",
        "_read_inputs",
        "read_inputs_",
    ],
)
def test_identifier_is_invalid(script_identifier):
    with pytest.raises(ScriptResolutionError, match="Invalid script"):
        validate_script_identifier(script_identifier)


# Rule: Discover local scripts


@pytest.mark.parametrize(
    ("location", "expected_scope"),
    [("shared", "shared"), ("job", "job"), ("nested_job", "job")],
)
def test_exactly_one_local_script_exists(tmp_path, location, expected_scope):
    project_root = tmp_path / "project"
    if location == "shared":
        expected_path = create_file(
            local_shared_script_path(project_root, "prepare.py")
        )
    elif location == "job":
        expected_path = create_file(
            local_job_script_path(project_root, "my-job", "prepare.py")
        )
    else:
        expected_path = create_file(
            local_job_script_path(
                project_root,
                "my-job",
                "helpers",
                "prepare.py",
            )
        )

    matches = find_local_scripts(project_root, "prepare")

    assert matches == [(expected_path, expected_scope)]


def test_no_local_script_exists(tmp_path):
    assert find_local_scripts(tmp_path / "project", "prepare") == []


def test_two_or_more_local_scripts_exist(tmp_path):
    project_root = tmp_path / "project"
    create_file(local_shared_script_path(project_root, "prepare.py"))
    create_file(local_job_script_path(project_root, "my-job", "prepare.py"))

    with pytest.raises(ScriptResolutionError, match="ambiguous in local"):
        resolve_script("prepare", project_root, tmp_path / "skill")


def test_ineligible_local_files_are_ignored(tmp_path):
    project_root = tmp_path / "project"
    create_file(
        local_shared_script_path(project_root, "prepare.txt"),
        content="ignored\n",
    )
    create_file(
        local_shared_script_path(project_root, "__pycache__", "prepare.py")
    )

    assert find_local_scripts(project_root, "prepare") == []


# Rule: Discover skill scripts


@pytest.mark.parametrize(
    ("location", "expected_scope"),
    [("shared", "shared"), ("job", "job"), ("nested_job", "job")],
)
def test_exactly_one_skill_script_exists(tmp_path, location, expected_scope):
    skill_root = tmp_path / "skill"
    if location == "shared":
        expected_path = create_file(skill_shared_script_path(skill_root, "prepare.py"))
    elif location == "job":
        expected_path = create_file(
            skill_job_script_path(skill_root, ("my-job",), "prepare.py")
        )
    else:
        expected_path = create_file(
            skill_job_script_path(
                skill_root,
                ("(authoring)", "my-job"),
                "helpers",
                "prepare.py",
            )
        )

    matches = find_skill_scripts(skill_root, "prepare")

    assert matches == [(expected_path, expected_scope)]


def test_no_skill_script_exists(tmp_path):
    assert find_skill_scripts(tmp_path / "skill", "prepare") == []


def test_two_or_more_skill_scripts_exist(tmp_path):
    project_root = tmp_path / "project"
    skill_root = tmp_path / "skill"
    create_file(skill_shared_script_path(skill_root, "prepare.py"))
    create_file(
        skill_job_script_path(
            skill_root,
            ("(authoring)", "my-job"),
            "prepare.py",
        )
    )

    with pytest.raises(ScriptResolutionError, match="ambiguous in skill"):
        resolve_script("prepare", project_root, skill_root)


def test_ineligible_skill_files_are_ignored(tmp_path):
    skill_root = tmp_path / "skill"
    create_file(skill_shared_script_path(skill_root, "prepare.json"), content="{}\n")
    create_file(skill_shared_script_path(skill_root, "__pycache__", "prepare.py"))
    create_file(skill_root / "jobs" / "my-job" / "prepare.py")

    assert find_skill_scripts(skill_root, "prepare") == []


# Rule: Prioritize local script


def test_valid_local_script_and_no_skill_script_returns_local(tmp_path):
    project_root = tmp_path / "project"
    skill_root = tmp_path / "skill"
    expected_path = create_file(local_shared_script_path(project_root, "prepare.py"))

    resolved = resolve_script("prepare", project_root, skill_root)

    assert resolved.script_path == expected_path
    assert resolved.source == "local"
    assert resolved.scope == "shared"


def test_valid_skill_script_and_no_local_script_returns_skill(tmp_path):
    project_root = tmp_path / "project"
    skill_root = tmp_path / "skill"
    expected_path = create_file(
        skill_job_script_path(
            skill_root,
            ("(authoring)", "my-job"),
            "prepare.py",
        )
    )

    resolved = resolve_script("prepare", project_root, skill_root)

    assert resolved.script_path == expected_path
    assert resolved.source == "skill"
    assert resolved.scope == "job"


def test_valid_local_and_skill_scripts_return_local(tmp_path):
    project_root = tmp_path / "project"
    skill_root = tmp_path / "skill"
    local_path = create_file(local_shared_script_path(project_root, "prepare.py"))
    create_file(
        skill_job_script_path(
            skill_root,
            ("(authoring)", "my-job"),
            "prepare.py",
        )
    )

    resolved = resolve_script("prepare", project_root, skill_root)

    assert resolved.script_path == local_path
    assert resolved.source == "local"


def test_ambiguous_local_scripts_and_valid_skill_script_fail_without_fallback(tmp_path):
    project_root = tmp_path / "project"
    skill_root = tmp_path / "skill"
    create_file(local_shared_script_path(project_root, "prepare.py"))
    create_file(local_job_script_path(project_root, "my-job", "prepare.py"))
    create_file(
        skill_job_script_path(
            skill_root,
            ("(authoring)", "my-job"),
            "prepare.py",
        )
    )

    with pytest.raises(ScriptResolutionError, match="ambiguous in local"):
        resolve_script("prepare", project_root, skill_root)


# Rule: Resolve script


def test_a_script_is_resolved_with_the_documented_result_fields(tmp_path):
    project_root = tmp_path / "project"
    skill_root = tmp_path / "skill"
    expected_path = create_file(local_shared_script_path(project_root, "prepare.py"))

    resolved = resolve_script("prepare", project_root, skill_root)

    assert resolved.identifier == "prepare"
    assert resolved.script_path == expected_path
    assert resolved.source == "local"
    assert resolved.scope == "shared"


def test_no_script_is_resolved(tmp_path):
    with pytest.raises(ScriptResolutionError, match="not found"):
        resolve_script("prepare", tmp_path / "project", tmp_path / "skill")
