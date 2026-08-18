---
name: desktop-wsl-apply-patch
description: Read this skill first before any repository command when an agent is running from a desktop app on Windows and controlling a WSL project. Use it for command execution, file discovery, bounded inspection, Node commands, the skill-local apply_patch script, encoded text, patch reports, and final-response links.
---

# Desktop WSL Apply Patch

Use this skill when Codex Apps on Windows controls a project that lives in WSL. The goal is a single repeatable workflow for discovery, inspection, command execution, Node commands, project-file edits, verification, and reporting without UNC or PowerShell surprises.

## Operating Loop

1. If the target file exists, read the target range with `sed -n -e 'start,end=' -e 'start,endp' path` to choose exact line numbers. If the target file is new, skip `sed`.
2. Resolve this skill's local folder path, then run `<skill-local-folder>/scripts/apply_patch` for one selected file.

    2.1. Send `read path start end` for an existing file range, or `read path 1 1` for a new file.

    2.2. Use the removal template printed by `<skill-local-folder>/scripts/apply_patch` as the old side.

    2.3. Send the matching addition hunk and let `<skill-local-folder>/scripts/apply_patch` apply it once.
3. If the target file exists after the edit, verify the edited range with `sed`.
4. End with `Files modified` and `Patch reports` using timestamped report links.

## Command Rules

### `grep` and `find`

- Agents MUST use `grep -n -e` or `grep -R -n -e` to locate relevant text when the target file or section is not already clear.
- Agents MUST always pass grep patterns through `-e`, even when the pattern does not start with a hyphen.
- Agents MUST use `find` for file discovery by name or path when needed.
- Agents MUST NOT use `rg` in this workspace.

```bash
wsl.exe -d distro -- grep -R -n -e "Operating Loop" desktop-wsl-apply-patch
wsl.exe -d distro -- find . -name 'SKILL.md'
```

### `sed`

- Agents MUST use `sed` for bounded reads and post-edit verification on existing files.
- Agents MUST skip `sed` before creation when the target file does not exist.
- Agents MUST choose exact line numbers with separate `-e` expressions: `sed -n -e '10,20=' -e '10,20p' path`.
- Agents MUST NOT use semicolon-separated `sed` expressions such as `{=;p}` in this environment.
- Agents MUST run one separate `sed` command per range instead of combining unrelated ranges.

```bash
wsl.exe -d distro -- sed -n -e '10,20=' -e '10,20p' path
wsl.exe -d distro -- sed -n -e '40,55=' -e '40,55p' path
```

### `<skill-local-folder>/scripts/apply_patch`

- Agents MUST use `<skill-local-folder>/scripts/apply_patch` as the only project-file edit path.
- Agents MUST resolve `<skill-local-folder>` from this skill's installed source location before invoking `scripts/apply_patch`.
- Agents MUST invoke `<skill-local-folder>/scripts/apply_patch` in an interactive PTY session, because the script reads patch instructions from stdin after startup.
- Agents MUST use the prepared flow for all file edits: start `<skill-local-folder>/scripts/apply_patch`, send `read path start end`, wait for the removal template, then send matching addition hunks.
- Agents MUST use `read path 1 1` for new files; the script determines that the file is missing and creates it from the same addition-hunk flow.
- Agents MUST keep each patch invocation to exactly one project file; this entire flow applies to one edited file at a time.
- If multiple files must change, agents MUST run the full flow separately for each file so each file has its own timestamped patch report.
- Agents MUST NOT edit project files with `sed -i`, `perl -pi`, Python rewrite scripts, shell redirection, or ad hoc wrappers.
- Agents MUST halt, report the exact failure, and avoid alternate edit paths when any step fails.
- Agents SHOULD use file names and paths without spaces when working with `apply_patch` `read` command; hyphens or underscores SHOULD be used instead. This is a current limitation of the `apply_patch` tool. If an edit requires a file or path containing spaces, agents MUST stop execution and notify the user.

Example:

```bash
wsl.exe -d distro -- <skill-local-folder>/scripts/apply_patch
```

```text
read desktop-wsl-apply-patch/SKILL.md 12 18
@@
+replacement line
```

```text
read new-file.md 1 1
@@
+first line
```

### `<skill-local-folder>/scripts/node`

- Agents MUST use `<skill-local-folder>/scripts/node` for project Node commands in Codex Apps on Windows controlling WSL.
- Agents MUST resolve `<skill-local-folder>` from this skill's installed source location before invoking `scripts/node`.
- Agents MUST NOT invoke `node` directly or through `bash -ic "node ..."` when `<skill-local-folder>/scripts/node` exists.
- Agents MUST halt and report the exact failure when `<skill-local-folder>/scripts/node` is missing or fails.

Example:

```bash
wsl.exe -d distro -- <skill-local-folder>/scripts/node .scripts/script.mjs
```

### Other Commands

- Agents MUST assume the shell already starts in the project root; agents MUST NOT run `cd` to enter the project before project-local commands.
- Agents MUST run WSL commands through `wsl.exe -d distro -- command`.
- Agents MUST prefer direct binaries over unnecessary shell wrappers such as `bash -c` or `bash -ic`; `scripts/node` is the Node-specific exception.
- Agents MUST NOT use shell pipes in direct WSL commands; agents MUST run separate commands instead.
- Agents MUST NOT use escaped quotes inside direct Windows-to-WSL command arguments; escaped quotes can be reinterpreted before reaching WSL. Use simpler patterns instead.
- Agents MUST use `/mnt/c/...` paths for files outside the project instead of direct PowerShell or UNC reads.

### User-Facing Narration

- Agents MUST keep narration minimal during routine `scripts/apply_patch` operations.
- Agents MUST announce only meaningful transitions, such as a blocker, a failed patch, a verification issue, or total edit completion.
- Agents MUST NOT narrate every mechanical stdin step in the prepared patch flow when the operation is proceeding normally.

## Prepared Patch

This section defines the format and rules for Operating Loop step 2, after `desktop-wsl-apply-patch/scripts/apply_patch` has printed the removal template and is waiting for matching addition hunks.

Addition hunk shape:

@@
+new text

Rules:

- Agents MUST send only addition hunks at this point; agents MUST NOT write the old side by hand.
- Agents MUST prefix each added line with one plus. If the new file line starts with minus (-), the patch line starts with plus then minus (+-).
- The returned addition hunk count MUST match the printed removal hunk count.
- Multiple `@@` hunks MAY target the same file, in the same order as the printed template.
- Agents MUST NOT hand-count unified diff headers.

## Simple Change Example

1. Inspect the target range with line numbers when the file exists:

```bash
wsl.exe -d distro -- sed -n -e '10,20=' -e '10,20p' desktop-wsl-apply-patch/SKILL.md
```

2. Start the prepared patch flow:

```bash
wsl.exe -d distro -- desktop-wsl-apply-patch/scripts/apply_patch
```

3. Send the `read` instruction to `desktop-wsl-apply-patch/scripts/apply_patch`. Use `read path 1 1` when the file is new.

```text
read desktop-wsl-apply-patch/SKILL.md 12 18
```

4. After `desktop-wsl-apply-patch/scripts/apply_patch` prints the removal template, send the matching addition hunk:

```diff
@@
+replacement line 1
+replacement line 2
```

5. Verify the edited range when the file exists:

```bash
wsl.exe -d distro -- sed -n '12,18p' desktop-wsl-apply-patch/SKILL.md
```

## Multi-Hunk Change Example

1. Inspect each range with a separate `sed` command:

```bash
wsl.exe -d distro -- sed -n -e '10,18=' -e '10,18p' desktop-wsl-apply-patch/SKILL.md
wsl.exe -d distro -- sed -n -e '35,45=' -e '35,45p' desktop-wsl-apply-patch/SKILL.md
```

2. Start the prepared patch flow for one file:

```bash
wsl.exe -d distro -- desktop-wsl-apply-patch/scripts/apply_patch
```

3. Send one `read` instruction with multiple ranges from the same file:

```text
read desktop-wsl-apply-patch/SKILL.md 12 18 36 42
```

4. Send the same number of addition hunks, in the same order:

```diff
@@
+replacement block one
@@
+replacement block two
```

5. Verify each changed range with separate `sed` commands.


## Encoded Text

Use encoded tokens when literal text could be interpreted by PowerShell, Bash, Python, Markdown, or `desktop-wsl-apply-patch/scripts/apply_patch` decoding.

| Character | Token |
| --- | --- |
| Newline | {{CHR:10}} |
| Backtick | {{CHR:96}} |
| Double quote | {{CHR:34}} |
| Single quote | {{CHR:39}} |
| Dollar sign in shell literals | {{CHR:36}} |
| Less-than | {{CHR:60}} |
| Greater-than | {{CHR:62}} |
| Backslash | {{CHR:92}} |
| Literal token braces in documentation | {{CHR:123}} and {{CHR:125}} |

Inside Python or tests, prefer `chr(10)` for newlines and `chr(96)` for backticks when that avoids shell interpretation.

## Patch Reports

`desktop-wsl-apply-patch/scripts/apply_patch` writes patch reports for patch operations:

- .patch-reports/latest.patch
- .patch-reports/timestamped-name.patch

Final responses after edits must end with this structure. The response itself MUST NOT wrap this final section in a code block; this block is documentation only.

```text
Files modified:
- [relative/path/to/file](//wsl.localhost/distro/home/user/projects/project/relative/path/to/file)
- [relative/path/to/other-file](//wsl.localhost/distro/home/user/projects/project/relative/path/to/other-file)

Patch reports:
- [relative/path/to/file](//wsl.localhost/distro/home/user/projects/project/.patch-reports/YYYYMMDDTHHMMSSZ.patch)
- [relative/path/to/other-file](//wsl.localhost/distro/home/user/projects/project/.patch-reports/YYYYMMDDTHHMMSSZ.patch)
```

Example:

```text
Files modified:
- [desktop-wsl-apply-patch/SKILL.md](//wsl.localhost/distro/home/user/projects/gtd/desktop-wsl-apply-patch/SKILL.md)

Patch reports:
- [desktop-wsl-apply-patch/SKILL.md](//wsl.localhost/distro/home/user/projects/gtd/.patch-reports/20260816T185223Z.patch)
```

Use timestamped patch report links in final responses, not latest.patch. Each patch report link must correspond to exactly one edited file.

## Verification

- Review the Changed files and Unified diff output from `desktop-wsl-apply-patch/scripts/apply_patch` before reporting completion.
- Verify edited content with sed after applying the patch.
- Run focused tests when the edited code has tests or behavior risk.
