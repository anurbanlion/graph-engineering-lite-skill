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
4. Save the evaluation as a Markdown review artifact.

## Output

A Markdown review using this template:

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
