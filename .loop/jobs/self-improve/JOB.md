# Self-Improve

## Description

Propose improvements to the loop system using evidence from the completed work, reports, and review.

## Input

- The assigned task and relevant execution context;
- Workspace Agent reports and linked artifacts;
- Review artifacts;
- The current `loop/SKILL.md` file.

## Process

1. Read the execution context, Workspace Agent reports, review artifacts, and `loop/SKILL.md`.
2. Identify a concrete improvement supported by the evidence.
3. Define the smallest specific proposal for the relevant Job, Rule, or skill artifact.
4. New improvement findings MUST remain proposals. A Reformer MUST NOT implement a proposed change to a Job, Rule, or Skill unless the user explicitly requests implementation of that specific change.
5. Reuse this Reformer subagent's existing self-improvement proposal when one is present. Update it in place across the Reformer’s subsequent turns by adding newly discovered proposals, revising existing proposals, and removing proposals whose corresponding improvements have been applied. The Reformer MUST NOT create a separate self-improvement report for remediation rounds of the same task. A task MAY have multiple Reformer subagents, and each Reformer MAY create and maintain its own proposal.
6. Save the current outstanding proposals as the Markdown improvement report. When the report recommends a change to a `SKILL.md`, it MUST include the exact unified diff patch for that proposed skill change. During proposal-only work, the self-improve job MUST NOT directly edit the `SKILL.md`; the patch is proposed in the report only.

## Output

A living Markdown improvement proposal containing only this Reformer subagent's current outstanding proposals. New findings remain proposals unless the user explicitly authorizes their implementation. When that Reformer has an existing proposal, the job MUST update it in place rather than create another report. A distinct Reformer MAY maintain a separate proposal for the same task. Include only sections that contain proposals. When proposing a `SKILL.md` change, the report MUST include its exact unified diff patch and MUST state that the skill file itself was not edited during proposal-only work.

```md
# Self-Improve Proposal - <task>

## Job Proposals

### Modify Job

- Target: [<job>](<link>)
- Proposed change: <specific replacement, addition, or removal>
- Reason: <evidence-supported rationale>

### Add Job

- Path: `.loop/jobs/<new-job>/JOB.md`
- Description: <purpose of the new Job>
- Input: <required inputs>
- Process: <proposed process>
- Output: <proposed output>
- Reason: <evidence-supported rationale>

## Rule Proposals

### Modify Rule

- Domain: `global` or `<domain>`
- Target: [<rule>](<link>)
- Proposed change: <specific replacement, addition, or removal>
- Reason: <evidence-supported rationale>

### Add Rule

- Domain: `global` or `<domain>`
- Path: `.loop/artifacts/<domain>/RULES.md`
- Proposed instruction: <rule text>
- Reason: <evidence-supported rationale>

## Skill Proposals

### Modify Description

- Target: [loop/SKILL.md](<link>)
- Proposed description: <replacement description>
- Reason: <evidence-supported rationale>

### Modify Skill Instructions

- Target section: `<section>`
- Proposed change: <specific replacement, addition, or removal>
- Reason: <evidence-supported rationale>
```
