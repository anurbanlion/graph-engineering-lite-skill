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
4. Save the proposals as a Markdown improvement report.

## Output

A Markdown improvement proposal using this template. Include only sections that contain proposals.

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
- Path: `.loop/rules/<domain>/RULES.md`
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
