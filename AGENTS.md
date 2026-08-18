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

## Codex Desktop WSL workflow

The locally installed copy of the `desktop-wsl-apply-patch` skill MUST be treated as canonical for this repository. Agents MUST NOT use a global copy of that skill when the locally installed copy exists.

- When running in Codex Desktop and controlling this repository through WSL, agents MUST read the `desktop-wsl-apply-patch` skill before running any repository command.
- Agents MUST read the `desktop-wsl-apply-patch` skill with `wsl.exe -d Ubuntu-26.04 -- cat <skill-local-folder>/desktop-wsl-apply-patch/SKILL.md`.

## Command rules

- Agents MUST NOT run `git push`.

# Extra

- Agents MUST NOT use graphify in this repository.