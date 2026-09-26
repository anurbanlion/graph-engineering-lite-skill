# Worker 6 — New Journey

Durable role guide for the new journey route shell and its handoff to journey integration.

## Responsibility

Worker 6 owns the route-shell job for the new journey. The shell lives in `page.tsx` and establishes this composition order:

`Navbar → journey composition point → PreFooterBanner → Footer`

The historical label **“T1 route shell” is Worker 6’s route-shell job**, not a separate worker or ownership lane. References may use `W6A / T1 — Route shell`, but must attribute the work to Worker 6.

Worker 6 hands the route structure to Worker 7. Worker 7 owns integration of the published organism, `propsEngine`, and trackers. Worker 6 does not own organism implementation, analytics wiring, global organism-barrel publication, or atom/molecule work.

## Authoritative references

- [Global rules](../../../rules/RULES.md): import boundaries, organism conventions, and required diff validation.
- [Dependency diagram](../dependency-diagram.md): W6A route-shell definition and the `W6 → W7` dependency.

When this guide conflicts with either reference, follow the authoritative project rule or dependency artifact and preserve the ownership boundary above.

## Durable rules and pointers

- Reuse the existing `Navbar`, `PreFooterBanner`, and `Footer`; do not create route-local duplicates.
- Keep the shell structural. Do not invent organism props, `propsEngine`, analytics schemas, or tracker wiring for Worker 7.
- Preserve the shell order: `Navbar` first, `PreFooterBanner` immediately before `Footer`.
- Organisms are exported from `src/shared/components/organisms/index.ts` and live under `src/shared/components/organisms/<organism>/`.
- Atoms, molecules, and organisms must use `@shared/` utilities when they need shared code. Follow the repository alias/import standards for route code.
- Do not edit `dependency-diagram.md` to record local implementation preferences.
- After repository changes or review, run the exact validation below:

  ```powershell
  git -c core.autocrlf=false -c core.whitespace=cr-at-eol diff --check
  ```

## Useful queries and commands

Use these questions to resolve ownership quickly:

- **What is W6A?** The `page.tsx` route shell with `Navbar`, the journey composition point, `PreFooterBanner`, and `Footer`.
- **Who is T1?** No separate worker; “T1 route shell” is the historical label for Worker 6’s W6A job.
- **Who integrates the organism into the shell?** Worker 7, after the organism is published.
- **Where does Worker 6 stop?** At route structure; organism props, trackers, and production-journey alignment belong to Worker 7.

PowerShell commands for focused inspection and validation:

```powershell
Get-Content -Raw '.loop/artifacts/RULES.md'
Get-Content -Raw '.loop/orchestration/guidelines-migration/dependency-diagram.md'
Get-ChildItem -Path '.loop/orchestration/guidelines-migration' -Filter 'README*.md' -File
git -c core.autocrlf=false -c core.whitespace=cr-at-eol diff --check
```

## Pitfalls

- Treating `T1` as another worker creates duplicate ownership and an ambiguous handoff.
- Reversing `PreFooterBanner` and `Footer` changes the expected shell composition.
- Pulling organism implementation, `propsEngine`, or analytics into W6 blurs the W6/W7 boundary.
- Introducing route-local copies of shared layout pieces bypasses the existing component system.
- Changing the dependency diagram for an implementation detail is outside this role.
- Do not run project `npm` scripts unless explicitly requested; the required check for this work is the Git diff validation above.

## Handoff guidance

- [ ] Confirm the target `page.tsx` is the new journey route.
- [ ] Confirm the shell order is `Navbar → journey composition → PreFooterBanner → Footer`.
- [ ] Confirm the three layout pieces are the existing components, not local duplicates.
- [ ] Leave a clear composition point for Worker 7’s published-organism integration.
- [ ] Keep organism props, `propsEngine`, trackers, and organism-barrel changes out of the route-shell scope.
- [ ] Check imports against the repository alias rules and `@shared/` boundary.
- [ ] Run `git -c core.autocrlf=false -c core.whitespace=cr-at-eol diff --check`.
- [ ] Verify `dependency-diagram.md` remains unchanged.
- [ ] Tell Worker 7 that the route-shell handoff is from Worker 6 / W6A, with “T1” only as the historical job label.
