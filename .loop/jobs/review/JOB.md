# Review

## Description

Evaluate completed work and its reports against the assigned task, applicable Rules, and assigned Jobs.

## Input

- The assigned task;
- Relevant Rules and Jobs;
- Workspace Agent reports and their linked artifacts.

## Process

1. Read the assigned task, relevant Rules, Jobs, reports, and linked artifacts.
2. Compare the completed work with the task and applicable requirements.
3. Identify verified outcomes, gaps, risks, and required corrections.
4. Each Reviewer MUST maintain one living review for each logical assigned task. If the Reviewer re-reviews corrections for the same task, it MUST update that review in place rather than create another review.

## Output

One living Markdown review for the logical assigned task, using this template:

```md
# Review - <task>

## Verdict

<Approved | Changes Required>

## Verified Outcomes

- <verified outcome and evidence>

## Findings

| Severity | Finding | Evidence | Required Correction |
| --- | --- | --- | --- |
| <severity> | <finding> | <link or observation> | <correction> |

## Required Corrections

- <correction or `None`>
```
