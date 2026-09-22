# Self-Improve Proposal - /root/improvement

## Job Proposals

### Modify Job - migrate-organism-into-journey

- Target: [migrate-organism-into-journey](jobs/components/migrate-organism-into-journey/JOB.md)
- Proposed change: Add a required discovery step before editing: build one targeted evidence bundle containing the applicable rules, analytics documentation when tracking is in scope, the public organism API and `propsEngine`, the target journey page, the reference-only implementation, and a direct-renderer inventory for every shared API that will change. The worker MUST reuse that recorded inventory rather than rediscovering callers after the API edit.
- Reason: The implementation report records several overlapping reads and a separate later renderer search. The final review confirmed that a single initial `rg -l '<CommonQuestions' app src --glob '!**/*.stories.*'` found the exact five production renderers and would have made the shared API migration both complete and cheaper to execute.

Exact unified diff patch:

```diff
diff --git a/.loop/jobs/components/migrate-organism-into-journey/JOB.md b/.loop/jobs/components/migrate-organism-into-journey/JOB.md
--- a/.loop/jobs/components/migrate-organism-into-journey/JOB.md
+++ b/.loop/jobs/components/migrate-organism-into-journey/JOB.md
@@ -27,7 +27,8 @@
 ## Process
 
-1. Inspect the shared organism's local `index.ts` and the shared-organisms barrel. Import the organism through `@shared/components/organisms` and use its supported public API.
-2. Inspect the old rendering only for the content, configuration, visual mode/layout, behavior, and ready analytics configuration that this migration must preserve.
-3. Replace the old rendering with the shared organism. Map the journey data and configuration, using `propsEngine` when available.
-4. Preserve the agreed visual mode, layout, user behavior, and ready analytics configuration. During journey migrations, use `io-mt-xl-*` for large-screen margin utilities; when replacing an existing `io-mt-lg-<number>` utility, retain its number and change only the breakpoint prefix to `io-mt-xl-<number>`. Record every approved difference.
-5. Run the `report` Job. The Worker MUST maintain one living report for this logical task and update it in place for corrections.
+1. Build and record a targeted evidence bundle before editing: applicable rules; analytics documentation when tracking is in scope; the public organism API and `propsEngine`; the target journey page; the reference-only implementation; and a direct-production-renderer inventory for every shared API that will change. The Worker MUST reuse the recorded inventory rather than rediscovering callers after the API edit.
+2. Inspect the shared organism's local `index.ts` and the shared-organisms barrel. Import the organism through `@shared/components/organisms` and use its supported public API.
+3. Inspect the old rendering only for the content, configuration, visual mode/layout, behavior, and ready analytics configuration that this migration must preserve.
+4. Replace the old rendering with the shared organism. Map the journey data and configuration, using `propsEngine` when available.
+5. Preserve the agreed visual mode, layout, user behavior, and ready analytics configuration. During journey migrations, use `io-mt-xl-*` for large-screen margin utilities; when replacing an existing `io-mt-lg-<number>` utility, retain its number and change only the breakpoint prefix to `io-mt-xl-<number>`. Record every approved difference.
+6. Run the `report` Job. The Worker MUST maintain one living report for this logical task and update it in place for corrections.
```

### Modify Job - migrate-analytics-to-shared-organism

- Target: [migrate-analytics-to-shared-organism](jobs/analytics/migrate-analytics-to-shared-organism/JOB.md)
- Proposed change: Before changing an organism's public analytics contract, require one scoped production-renderer search, excluding Storybook, and record the full caller list in the report. The worker MUST update each recorded applicable renderer as part of the same change.
- Reason: Splitting the FAQ interaction target required changes in five direct production renderers. The analytics rule already requires their configuration; making the one-time inventory an explicit job step prevents repeated searches and gives the reviewer compact completeness evidence.

Exact unified diff patch:

```diff
diff --git a/.loop/jobs/analytics/migrate-analytics-to-shared-organism/JOB.md b/.loop/jobs/analytics/migrate-analytics-to-shared-organism/JOB.md
--- a/.loop/jobs/analytics/migrate-analytics-to-shared-organism/JOB.md
+++ b/.loop/jobs/analytics/migrate-analytics-to-shared-organism/JOB.md
@@ -27,9 +27,10 @@
 ## Process
 
 1. Read the analytics domain rules and `analytics/docs/` before making changes.
-2. Audit the old component's user actions, event names, event data, and journey-level configuration. Add this audit to the same living Worker report; it MUST directly drive the implementation.
-3. Search for a compatible existing schema. If none exists, define and register the required schema in the common registry for a reusable/shared organism.
-4. Add the organism's supported optional `analytics` API. Its `TrackingTarget` context MUST contain only data the organism can provide.
-5. Wire tracking with `TrackedAction` for clickable controls or `useTracking` for logic-driven events. Remove a legacy callback when its only purpose is to forward the same analytics data and it has no other consumer.
-6. Find every direct production caller that must opt in and configure the required tracker. Storybook-only callers MUST be excluded.
-7. Run the `report` Job. The Worker MUST maintain one living report for this logical task and update it in place for corrections.
+2. Before changing the organism's public analytics contract, run one scoped search for every direct production renderer that must opt in; Storybook-only callers MUST be excluded. Record the complete caller list in the living Worker report.
+3. Audit the old component's user actions, event names, event data, and journey-level configuration. Add this audit to the same living Worker report; it MUST directly drive the implementation.
+4. Search for a compatible existing schema. If none exists, define and register the required schema in the common registry for a reusable/shared organism.
+5. Add the organism's supported optional `analytics` API. Its `TrackingTarget` context MUST contain only data the organism can provide.
+6. Wire tracking with `TrackedAction` for clickable controls or `useTracking` for logic-driven events. Remove a legacy callback when its only purpose is to forward the same analytics data and it has no other consumer.
+7. Configure the required tracker at every recorded direct production renderer.
+8. Run the `report` Job. The Worker MUST maintain one living report for this logical task and update it in place for corrections.
```

### Modify Job - self-improve

- Target: [self-improve](jobs/self-improve/JOB.md)
- Proposed change: Require an exact unified diff patch for every proposal that modifies a `.loop/jobs/**/JOB.md` file or a `SKILL.md`; add the corresponding fenced `diff` field to each Job and Skill Proposal template; require report titles to use the Reformer subagent identifier and Modify-Job headings to include the target Job name; and require every Job, Rule, and Skill proposal Target to be a functional Markdown link using a path relative to the self-improvement report. Keep the existing requirement that proposal-only work does not edit the actual Job or skill file.
- Reason: The job prose previously required an exact patch only for `SKILL.md`, and its template did not visibly request one. This report's earlier prose-only Job proposals and omitted Loop-skill patch show that both types need a mechanically explicit template requirement. Identifying the Reformer and each modified Job directly in headings also makes living proposals easier to route and review.

Exact unified diff patch:

```diff
diff --git a/.loop/jobs/self-improve/JOB.md b/.loop/jobs/self-improve/JOB.md
--- a/.loop/jobs/self-improve/JOB.md
+++ b/.loop/jobs/self-improve/JOB.md
@@ -18,8 +18,8 @@
 3. Define the smallest specific proposal for the relevant Job, Rule, or skill artifact.
 4. New improvement findings MUST remain proposals. A Reformer MUST NOT implement a proposed change to a Job, Rule, or Skill unless the user explicitly requests implementation of that specific change.
 5. Reuse this Reformer subagent's existing self-improvement proposal when one is present. Update it in place across the Reformer’s subsequent turns by adding newly discovered proposals, revising existing proposals, and removing proposals whose corresponding improvements have been applied. The Reformer MUST NOT create a separate self-improvement report for remediation rounds of the same task. A task MAY have multiple Reformer subagents, and each Reformer MAY create and maintain its own proposal.
-6. Save the current outstanding proposals as the Markdown improvement report. When the report recommends a change to a `SKILL.md`, it MUST include the exact unified diff patch for that proposed skill change. During proposal-only work, the self-improve job MUST NOT directly edit the `SKILL.md`; the patch is proposed in the report only.
+6. Save the current outstanding proposals as the Markdown improvement report. When the report recommends a modification to a `.loop/jobs/**/JOB.md` file or a `SKILL.md`, it MUST include the exact unified diff patch for that proposed change. Every Job, Rule, and Skill proposal Target MUST be a functional Markdown link using a path relative to the self-improvement report. During proposal-only work, the self-improve job MUST NOT directly edit the actual Job or skill file; the patch is proposed in the report only.
 
 ## Output
 
-A living Markdown improvement proposal containing only this Reformer subagent's current outstanding proposals. New findings remain proposals unless the user explicitly authorizes their implementation. When that Reformer has an existing proposal, the job MUST update it in place rather than create another report. A distinct Reformer MAY maintain a separate proposal for the same task. Include only sections that contain proposals. When proposing a `SKILL.md` change, the report MUST include its exact unified diff patch and MUST state that the skill file itself was not edited during proposal-only work.
+A living Markdown improvement proposal containing only this Reformer subagent's current outstanding proposals. New findings remain proposals unless the user explicitly authorizes their implementation. When that Reformer has an existing proposal, the job MUST update it in place rather than create another report. A distinct Reformer MAY maintain a separate proposal for the same task. Include only sections that contain proposals. The title MUST use `# Self-Improve Proposal - <reformer-subagent-identifier>`, every Modify Job heading MUST use `### Modify Job - <job-name>`, and every Job, Rule, and Skill proposal Target MUST be a functional Markdown link using a path relative to the self-improvement report. When proposing a modification to a `.loop/jobs/**/JOB.md` file or a `SKILL.md`, the report MUST include its exact unified diff patch and MUST state that the actual Job or skill file was not edited during proposal-only work.
@@ -27,19 +27,29 @@
 ```md
-# Self-Improve Proposal - <task>
+# Self-Improve Proposal - <reformer-subagent-identifier>
 
 ## Job Proposals
 
-### Modify Job
+### Modify Job - <job-name>
 
- - Target: [<job>](<link>)
+ - Target: [<job-name>](<functional relative path>)
 - Proposed change: <specific replacement, addition, or removal>
 - Reason: <evidence-supported rationale>
+- Exact unified diff patch:
+  ```diff
+  diff --git a/<job-path> b/<job-path>
+  ...
+  ```
 
 ### Add Job
 
- - Path: `.loop/jobs/<new-job>/JOB.md`
+ - Target: [<job-name>](<functional relative path>)
 - Description: <purpose of the new Job>
 - Input: <required inputs>
 - Process: <proposed process>
 - Output: <proposed output>
 - Reason: <evidence-supported rationale>
+- Exact unified diff patch:
+  ```diff
+  diff --git a/<job-path> b/<job-path>
+  ...
+  ```
@@ -47,30 +57,41 @@
 ## Rule Proposals
 
 ### Modify Rule
 
- Target: [<rule>](<link>)
+ Target: [<rule-name>](<functional relative path>)
 - Proposed change: <specific replacement, addition, or removal>
 - Reason: <evidence-supported rationale>
 
 ### Add Rule
 
 - Domain: `global` or `<domain>`
- Path: `.loop/rules/<domain>/RULES.md`
+ Target: [<rule-name>](<functional relative path>)
 - Proposed instruction: <rule text>
 - Reason: <evidence-supported rationale>
 
 ## Skill Proposals
 
 ### Modify Description
 
- - Target: [loop/SKILL.md](<link>)
+ - Target: [<skill-name>](<functional relative path>)
 - Proposed description: <replacement description>
 - Reason: <evidence-supported rationale>
+- Exact unified diff patch:
+  ```diff
+  diff --git a/<skill-path> b/<skill-path>
+  ...
+  ```
 
 ### Modify Skill Instructions
 
+ - Target: [<skill-name>](<functional relative path>)
 - Target section: `<section>`
 - Proposed change: <specific replacement, addition, or removal>
 - Reason: <evidence-supported rationale>
+- Exact unified diff patch:
+  ```diff
+  diff --git a/<skill-path> b/<skill-path>
+  ...
+  ```
```

## Rule Proposals

### Modify Rule

- Domain: `global`
- Target: [global rules](rules/RULES.md)
- Proposed change: Replace the placeholder with: `When code must derive a text value from paired plain-text and rich-text props, it MUST use getTextFromPlainOrRichText(text, richText) from src/shared/utils/richtext/richtext.util.ts. It MUST NOT add a local resolver or repeat a plain-text fallback around extractTextFromRichText.`
- Reason: `extractTextFromRichText` and `getTextFromPlainOrRichText` are now canonical shared utilities. Shared consumers were migrated from the legacy `@/utils/richText` path, which is retained only as a compatibility re-export; centralizing this rule prevents new helpers such as `getTrackLabel` and inconsistent fallback expressions.

Exact unified diff patch:

```diff
diff --git a/.loop/rules/RULES.md b/.loop/rules/RULES.md
--- a/.loop/rules/RULES.md
+++ b/.loop/rules/RULES.md
@@ -1 +1 @@
-No rules for the moment
+When code must derive a text value from paired plain-text and rich-text props, it MUST use `getTextFromPlainOrRichText(text, richText)` from `src/shared/utils/richtext/richtext.util.ts`. It MUST NOT add a local resolver or repeat a plain-text fallback around `extractTextFromRichText`.
```

### Modify Rule

- Domain: `analytics`
- Target: [analytics rules](rules/analytics/RULES.md)
- Proposed change: Add five reusable analytics conventions: action-specific organism context types; concise schema purpose and `event_data` comments; reuse of `common.ctaClicked` for equivalent reusable CTA contracts; completed-action analytics slot names; and named tracking handlers rather than inline tracking calls in JSX.
- Reason: `CommonQuestions` now retains action-specific contexts while its CTA schema is consolidated into `common.ctaClicked`; organism slots use `stepClicked`, `ctaClicked`, and `questionOpened`; and `FeaturesSteps` routes its event through `handleStepOnClick`. Together, these changes make the shared analytics API consistent, reusable, and easier to audit.

Exact unified diff patch:

```diff
diff --git a/.loop/rules/analytics/RULES.md b/.loop/rules/analytics/RULES.md
--- a/.loop/rules/analytics/RULES.md
+++ b/.loop/rules/analytics/RULES.md
@@ -3,4 +3,9 @@
 - Agents and Orchestrators MUST read the relevant documentation in `analytics/docs/` before implementing or reviewing analytics taggeos.
 - When an implementation introduces an optional analytics prop on an organism component, agents MUST search for its direct production page renderers and configure the tracker at each applicable renderer before reporting the work complete. Storybook-only renderers MUST be excluded.
 - Trackers for reusable or shared components MUST be defined and registered in the common schema registry with the common tracker namespace. Journey-specific registries MUST only contain trackers owned by that journey.
 - When `TrackedAction` provides an interaction's analytics behavior, agents MUST remove any legacy callback prop and invocation whose only payload is tracking context and which has no remaining non-analytics consumer.
+- When an organism exposes more than one analytics interaction, it MUST define a distinct context type for each action-specific tracker and MUST name that type after the interaction or tracker. Each analytics prop and its `useTracking` or `TrackedAction` call MUST use its matching action-specific context type; an ambiguous shared context type MUST NOT be used across unrelated actions.
+- Analytics schemas MUST include concise comments that state the event's purpose and explain every `event_data` field. Comments MUST follow the established schema-comment style used by `header.schemas.ts`.
+- Reusable CTA interactions with the same event contract MUST use the registered common `common.ctaClicked` target. Agents MUST NOT create an action-specific CTA schema unless its event name or event-data contract differs.
+- Organism analytics slots MUST use completed-action names that describe the emitted interaction, such as `stepClicked`, `ctaClicked`, and `questionOpened`, rather than callback-oriented names.
+- An organism MUST call tracking from a named action handler that receives the interaction data; JSX controls MUST invoke that handler rather than invoke `useTracking` directly inline.
```

### Add Rule

- Domain: `components`
- Target: [component rules](rules/components/RULES.md)
- Proposed instruction: `Exported organism propsEngine functions MUST accept a nullable wrapper as their source input: propsEngine(source: Maybe<T>). They MUST use the source-domain type T appropriate to that organism (for example, Maybe<IoLiquidSectionV2>) rather than requiring a non-null source. For shared organisms covered by Storybook or component stories, parity verification MUST compare functional behavior, source-data mapping, and tracking equivalence. It MUST NOT require visual/style equivalence unless the migration explicitly changes the shared organism's visual contract.`
- Reason: The user clarified the props-engine convention is general, and the completed migration relied on the shared organism visual library. Centralizing both conventions prevents future signature drift and unnecessary visual-parity churn.

Exact unified diff patch:

```diff
diff --git a/.loop/rules/components/RULES.md b/.loop/rules/components/RULES.md
new file mode 100644
--- /dev/null
+++ b/.loop/rules/components/RULES.md
@@ -0,0 +1,3 @@
+# Component Rules
+
+- Exported organism `propsEngine` functions MUST accept a nullable wrapper as their source input: `propsEngine(source: Maybe<T>)`. They MUST use the source-domain type `T` appropriate to that organism (for example, `Maybe<IoLiquidSectionV2>`) rather than requiring a non-null source. For shared organisms covered by Storybook or component stories, parity verification MUST compare functional behavior, source-data mapping, and tracking equivalence. It MUST NOT require visual/style equivalence unless the migration explicitly changes the shared organism's visual contract.
```

## Skill Proposals

### Modify Skill Instructions

- Target: [loop skill](../.codex/skills/loop/SKILL.md)
- Target section: `Work`
- Proposed change: Add an explicit bounded-reuse instruction for Workspace Agents.
- Reason: Reusing an agent that already read its assigned Job and task evidence avoids repeated setup, commands, and tokens when the same Job receives distinct inputs across one orchestration.

Exact unified diff patch:

```diff
diff --git a/.codex/skills/loop/SKILL.md b/.codex/skills/loop/SKILL.md
--- a/.codex/skills/loop/SKILL.md
+++ b/.codex/skills/loop/SKILL.md
@@ -74,4 +74,5 @@
 ### Work
 
 1. After approval, you SHOULD delegate executable work to Workspace Agents and a prompt following the Subagent Prompt Template.
    - **Task**: A Workspace Agent MAY receive an ad-hoc task, one or more explicitly assigned Jobs, or both. The prompt MUST instruct the Workspace Agent to execute the `report` Job after completing its assigned task and Jobs, and return the report link to the Orchestrator.
+   - **Reuse**: For the same Job with distinct inputs, the Orchestrator SHOULD reuse the same Workspace Agent for up to three assignments so it retains Job and task context. This limit MUST NOT include correction or remediation rounds within the current loop, or assignments where the user explicitly directs a subagent to implement a specific task.
```

The loop skill itself was not edited; these are proposal-only changes.
