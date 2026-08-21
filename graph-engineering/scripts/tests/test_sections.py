import pytest

from lib.sections import extract_section

# ---------------------------------------------------------------
# Fixture: a realistic JOB.md with multiple sections
# ---------------------------------------------------------------

SAMPLE_JOB_MD = """\
# create-initiatives

Some preamble text.

## Inputs

The job MUST receive:

- a kebab-case `domain` where the compiled initiative index MUST be stored;
- a kebab-case `source-job-identifier` whose managed outputs define initiative candidates.

Examples:

```txt
domain: global
source-job-identifier: create-initiatives
```

## Process

1. Read the source job outputs.
2. Compile them into an index.
3. Write the index to the domain.

## Output

The job produces a Managed Output at `OUTPUT.md`.
"""

SAMPLE_NO_INPUTS = """\
# simple-job

## Process

Just do the thing.

## Output

Done.
"""

SAMPLE_TRAILING_SECTION = """\
# trailing

## Inputs

input-a
input-b
"""


# ---------------------------------------------------------------
# Tests: extract_section
# ---------------------------------------------------------------


class TestExtractSection:
    def test_extracts_inputs_section(self):
        result = extract_section(SAMPLE_JOB_MD, "## Inputs")
        assert "kebab-case `domain`" in result
        assert "source-job-identifier" in result

    def test_extracts_process_section(self):
        result = extract_section(SAMPLE_JOB_MD, "## Process")
        assert "Read the source job outputs" in result
        assert "Compile them into an index" in result

    def test_extracts_output_section(self):
        result = extract_section(SAMPLE_JOB_MD, "## Output")
        assert "Managed Output" in result

    def test_does_not_bleed_into_next_section(self):
        result = extract_section(SAMPLE_JOB_MD, "## Inputs")
        assert "Read the source job outputs" not in result
        assert "## Process" not in result

    def test_includes_heading_itself(self):
        result = extract_section(SAMPLE_JOB_MD, "## Inputs")
        assert result.startswith("## Inputs\n\n")

    def test_returns_empty_string_when_heading_not_found(self):
        result = extract_section(SAMPLE_JOB_MD, "## Nonexistent")
        assert result == ""

    def test_returns_empty_string_for_empty_content(self):
        result = extract_section("", "## Inputs")
        assert result == ""

    def test_handles_missing_section_in_document(self):
        result = extract_section(SAMPLE_NO_INPUTS, "## Inputs")
        assert result == ""

    def test_extracts_last_section_without_trailing_heading(self):
        result = extract_section(SAMPLE_TRAILING_SECTION, "## Inputs")
        assert "input-a" in result
        assert "input-b" in result

    def test_strips_leading_and_trailing_whitespace(self):
        result = extract_section(SAMPLE_JOB_MD, "## Inputs")
        assert not result.startswith("\n")
        assert not result.endswith("\n")

    def test_preserves_code_blocks(self):
        result = extract_section(SAMPLE_JOB_MD, "## Inputs")
        assert "```txt" in result
        assert "```" in result

    def test_heading_with_special_regex_chars(self):
        content = "## Inputs (required)\n\nsome data\n\n## Process\n\nstep 1\n"
        result = extract_section(content, "## Inputs (required)")
        assert "some data" in result
        assert "step 1" not in result
