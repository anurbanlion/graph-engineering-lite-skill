---
name: desktop-wsl-apply-patch
description: Use this skill to modify existing files and create new files in a WSL environment instead of apply_wsl.
---

When Codex for Windows edits a project in WSL, native `apply_patch` can have path and temporary-file failures. This wrapper avoids those failures while retaining native `apply_patch` to create the temporary patch file.

# Apply Patch

1. The agent MUST inspect the target with numbered output before any modification:

```bash
sed -n -e 'start,end=' -e 'start,endp' target
```

For multiple reads, run one command per range:

```bash
sed -n -e '10,18=' -e '10,18p' target
sed -n -e '40,50=' -e '40,50p' target
```

The agent MAY read the whole file or several ranges. The printed line numbers define the replacement ranges. The agent MUST NOT copy the old content into the temporary patch.

2. The agent MUST create `C:\Users\user\projects\patchs\apply.patch.temp` with the native `apply_patch` tool. This wrapper applies the target change, but the agent MUST still use native `apply_patch` to create the temporary patch file. It contains one or more replacement hunks:

```text
@@ 10 12
+replacement line
+another replacement line
```

For multiple hunks in the same target, include them in order in the same temporary patch:

```text
@@ 10 12
+first replacement
@@ 40 42
+second replacement
```

Every hunk replaces the inclusive range start-end. Lines may be created with or without a leading plus; the applicator normalizes them. Blank lines inside hunks are preserved.

3. The agent MUST run the script with the default temporary patch path and target file:

```bash
scripts/apply_patch /mnt/c/Users/user/projects/patchs/apply.patch.temp <target-file>
```

- If any problem occurs while using the script, the agent MUST stop execution immediately and MUST report the problem to the user.
- Script must be called from the local skill folder (ex. `.codex/skills/desktop-wsl-apply-patch/scripts...`)

4. The agent MUST verify the target after the script finishes. Verification confirms the result; it does not perform the application.

```bash
sed -n -e '10,18=' -e '10,18p' target
```

When multiple ranges were replaced, verify each one separately:

```bash
sed -n -e '10,18=' -e '10,18p' target
sed -n -e '40,50=' -e '40,50p' target
```

5. The agent MUST follow these safety rules:

- One target file per invocation.
- Ranges MUST be 1-based, ordered, non-overlapping, and within the current file.
- The script MUST abort before writing if any range is invalid.
- The default temporary file MUST be `C:\Users\user\projects\patchs\apply.patch.temp`.

6. Agents MUST report every file created, modified, regenerated, or restored at the end of each implementation response, with a concise description of the change.

```txt
Created or modified:

- [`working/scripts/execute.py`](working/scripts/execute.py): Added `{context.<campo>}` interpolation and removed initial `context` creation from snapshots.
- [`working/scripts/custom/compile-initiatives-tasks.py`](working/scripts/custom/compile-initiatives-tasks.py): Changed Project folder links to omit `file://`.
- [`.graph-engineering/runs/gtd-tool/add-tasks/OUTPUT-20260822-2318.md`](.graph-engineering/runs/gtd-tool/add-tasks/OUTPUT-20260822-2318.md): Updated the runtime interpolation tasks.
- [`working/scripts/custom/test.md`](working/scripts/custom/test.md): Regenerated the global initiative view.
- [NEW] [`working/tests/test_execute.py`](working/tests/test_execute.py): Added runtime interpolation tests.
```