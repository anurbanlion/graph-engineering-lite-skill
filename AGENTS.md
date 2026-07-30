NEVER USE git push.

# Collaboration guardrails

- If files changed between assistant responses, assume the user made those edits intentionally. Preserve them and work around them; only overwrite or restore previous structure when the user explicitly asks, or ask first if the change blocks the task.

# Commit Suggestions

- When suggesting a commit message, you MUST first inspect the relevant Git diff: `git diff --cached` for staged changes, `git diff` for unstaged changes, or both when needed.
- You MUST provide exactly three proposals using `feat`, `fix`, or `chore`, optionally with a scope.
- Each proposal MUST follow: `git commit -m "<message>"`.
- You MUST mark one as `Favorite` and explain why in one line.

Output:
```text
1. `git commit -m "feat(hero-banner): add responsive image metadata"`
2. `git commit -m "chore(hero-banner): simplify responsive image handling"`
3. `git commit -m "fix(hero-banner): align metadata with banner logic"`

Favorite: `feat(hero-banner): add responsive image metadata` because it best represents the user-visible capability.
```