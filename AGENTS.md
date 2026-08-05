- You MUST treat `graph-engineering` folder as a skill, that is, you must load its SKILL.md file in every session.

# Instructions style

- Every instruction written in this file MUST use RFC 2119 language. The key words MUST, MUST NOT, SHOULD, SHOULD NOT, and MAY in this file are to be interpreted as described by RFC 2119.

## Command rules

- Agents MUST NOT run `git push`.

## Collaboration guardrails

- If files change between assistant responses, agents MUST assume the user made those edits intentionally and MUST preserve those edits and work around them.
- Agents MUST NOT overwrite or restore earlier structure unless the user explicitly requests it.
- If those edits block the requested work, agents SHOULD ask for direction before proceeding.

## Commit suggestions

- Agents MUST suggest commit messages only when the user explicitly requests them.
- Before suggesting a commit message, agents MUST inspect the relevant Git diff: `git diff --cached` for staged changes and `git diff` for unstaged changes.
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

# Extra

- Agents MUST NOT use graphify in this repository.