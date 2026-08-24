# Instructions style

- Every instruction written in this file MUST use RFC 2119 language. The key words MUST, MUST NOT, SHOULD, SHOULD NOT, and MAY in this file are to be interpreted as described by RFC 2119.

## Collaboration guardrails

- If files change between assistant responses, agents MUST assume the user made those edits intentionally and MUST preserve those edits and work around them.
- Agents MUST NOT overwrite or restore earlier structure unless the user explicitly requests it.
- If those edits block the requested work, agents SHOULD ask for direction before proceeding.
- Collaboration guardrails MAY require reading the relevant files or ranges before editing when modification tools do not require prior reading, but MUST NOT be interpreted as requiring `git status` or similar repository status commands.

## Commit suggestions

- Agents MUST suggest commit messages only when the user explicitly requests them.
- Before suggesting a commit message, agents MUST inspect the relevant Git diff using strictly `git diff --cached` for staged changes and `git diff` for unstaged changes, and MUST NOT run redundant diff or status commands.
- Agents MUST provide exactly three proposals using `feat`, `fix`, or `chore`, optionally with a scope.
- Each proposal MUST follow: `git commit -m "<message>"`.
- Agents MUST mark one proposal as `Favorite` and explain why in one line.
- When the user selects one of the numbered proposals, that selection is authorization to create the selected commit. The agent MUST add the relevant files, then run the corresponding `git commit` command.

Example output:
```text
1. `git commit -m "feat(hero-banner): add responsive image metadata"`
2. `git commit -m "chore(hero-banner): simplify responsive image handling"`
3. `git commit -m "fix: align metadata with banner logic"`

Favorite: `feat(hero-banner): add responsive image metadata` because it best represents the user-visible capability.
```

## Instruction Clarification and Discrepancy Analysis

- When the user inquires why an action was omitted, failed, or deviated from expectations, agents MUST NOT provide generic apologies, excuses, or pass-off explanations such as "it was my mistake".
- Agents MUST assume discrepancies originate from ambiguities, gaps, or conflicting instructions in repository documentation or prompt rules.
- Agents MUST analyze the root cause by specifying how the current instructions were interpreted, citing the exact file, line number, or rule where the ambiguity or constraint occurred.
- Agents MUST propose concrete modifications (specifying file, line range, and proposed replacement text) to clarify the instruction so that future executions unambiguously produce the desired behavior.

### Example

When asked *"Why did you not perform X?"*, the agent response MUST follow this structure:

```text
The action was omitted because of the interpretation of [AGENTS.md:L60]:
- Current instruction: "<text of rule>"
- Interpretation: "<why this caused the agent not to do X>"

Proposed instruction update to align future behavior:
- Target: `AGENTS.md` (around line 60)
- Replace with:
  "<new clarified rule text>"
```

## Codex Desktop WSL workflow

When running Codex Desktop in Windows and controlling this repository through WSL:

- Agents MUST always read the `desktop-wsl-apply-patch` skill with `wsl.exe -d distro -- cat <skill-local-folder>/desktop-wsl-apply-patch/SKILL.md` at the start of any conversation.

The `<skill-local-folder>` variable is the folder on the current project where skills are located and its location depends on the agent (ex. `.codex/skills`)

## Command rules

- Agents MUST NOT run `git push`.

# Extra

- Agents MUST NOT use graphify in this repository.