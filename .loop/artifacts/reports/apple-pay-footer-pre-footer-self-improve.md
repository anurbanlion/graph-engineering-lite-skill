# Self-Improve Proposal - Apple Pay Footer and PreFooterBanner migration

## Skill Proposals

### Modify Skill Instructions

- Target: [loop/SKILL.md](../../.codex/skills/loop/SKILL.md)
- Target section: `Work` and `Post-Work`
- Proposed change: Add an explicit report-driven review loop: each workspace agent reports immediately after each assigned job, notifies the Orchestrator, and proceeds to its next assigned job. The Orchestrator dispatches a single reviewer as each incremental report becomes available; findings return only to the owning worker. After the implementation reviewer approves all workers, run joint parity; then dispatch the same reviewer for a final parity-review round before self-improvement.
- Reason: This migration required two component-owned paths (`PreFooterBanner` and `Footer`) that each completed analytics migration and journey wiring, reported at both boundaries, and then received reviewer feedback. The parity job exposed a Footer payload-key mismatch (`sub_section` versus legacy-compatible `subSection`) after the first review, requiring a targeted worker correction, parity rerun, and reviewer round 2. Encoding this feedback topology prevents prematurely treating a one-pass review as terminal.

```diff
diff --git a/.codex/skills/loop/SKILL.md b/.codex/skills/loop/SKILL.md
--- a/.codex/skills/loop/SKILL.md
+++ b/.codex/skills/loop/SKILL.md
@@
 ### Work
 
 1. After approval, you SHOULD delegate executable work to Workspace Agents and a prompt following the Subagent Prompt Template.
    - **Task**: A Workspace Agent MAY receive an ad-hoc task, one or more explicitly assigned Jobs, or both. The prompt MUST instruct the Workspace Agent to execute the `report` Job after completing its assigned task and Jobs, and return the report link to the Orchestrator.
+   - **Incremental reports**: When a Worker has multiple assigned Jobs, it MUST execute `report` after each job boundary specified by the Orchestrator, notify the Orchestrator with that report link, and then continue with its next assigned Job unless the Orchestrator directs otherwise. The report for one Worker MUST remain a living artifact across correction rounds.
+   - **Incremental review**: The Orchestrator SHOULD send each newly available Worker report to one designated Reviewer promptly. Review findings MUST be routed only to the Worker that owns the affected artifact; that Worker MUST update its living report and notify the Orchestrator after correction.
 
 ### Post-Work
 
 1. After the Workspace Agents complete their work and reports, you MUST delegate evaluation using the `review` Job and a prompt following the Subagent Prompt Template.
 
-2. After the review completes, you MUST delegate system improvement using the `self-improve` Job and a prompt following the Subagent Prompt Template.
+2. When the task has a final parity or verification job, the Orchestrator MUST run it after implementation review approval. The designated Reviewer MUST receive the resulting parity report for a final review round; parity findings MUST return to the parity Worker or affected owning Worker for correction and rerun before proceeding.
+
+3. After all required review rounds complete, you MUST delegate system improvement using the `self-improve` Job and a prompt following the Subagent Prompt Template.
```

### Modify Skill Instructions

- Target: [loop/SKILL.md](../../.codex/skills/loop/SKILL.md)
- Target section: `Post-Work`
- Proposed change: Require evidence plans to start from reports and permit source inspection only for a direct, unresolved report claim, changed artifact, or reviewer finding. Each report and review should state why any additional read/search was needed and avoid duplicate checks whose scope is unaffected by the correction.
- Reason: The reviewer completed correction re-review by reading the changed `TrackedAction` context and one scoped whitespace check, then completed reviewer round 2 with only the parity report, final worker reports, one schema/call-site check, and one whitespace check. This avoided rereading legacy pages, ten journey renderers, and unrelated PreFooterBanner evidence. The parity rerun used the same pattern. Making it explicit preserves confidence while reducing calls and broad file reads.

```diff
diff --git a/.codex/skills/loop/SKILL.md b/.codex/skills/loop/SKILL.md
--- a/.codex/skills/loop/SKILL.md
+++ b/.codex/skills/loop/SKILL.md
@@
 ### Post-Work
 
 1. After the Workspace Agents complete their work and reports, you MUST delegate evaluation using the `review` Job and a prompt following the Subagent Prompt Template.
+   - **Evidence minimization**: Reviewers and verification Workers MUST consume supplied living reports before source inspection. They MUST limit additional reads, searches, and commands to artifacts directly cited by an unresolved claim, changed by a correction, or required to validate a finding. They MUST NOT repeat evidence checks that the report shows are unaffected by the current change, and SHOULD record the necessity and scope of each additional check in their report.
```

The skill file itself was not edited during this proposal-only work.
