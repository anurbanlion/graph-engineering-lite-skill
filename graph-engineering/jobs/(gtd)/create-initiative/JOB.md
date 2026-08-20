# Create Initiative

## Objective

The job MUST create a project charter for an initiative through an iterative conversation with the user.

The charter MUST establish the initiative's title, description, and additional global context that helps both the user and the agent understand the initiative's purpose, boundaries, and current situation.

## Inputs

The job MAY receive any combination of the following optional inputs, including none of them:

- An initial idea, need, or opportunity;
- A proposed initiative title;
- A proposed initiative domain;
- Prior conversation, notes, constraints, or related context.

The agent MUST use the interview to establish any information that is not provided or remains unresolved.

When a domain is provided, the agent MUST evaluate it and MAY suggest a different kebab-case domain when it better represents the initiative.

## Process

**1. Receive Initial Context**

1. The agent MUST identify and preserve any idea, need, opportunity, title, domain, or related context already provided by the user.
2. The agent MUST NOT repeat an initial question when the user has already answered it.

**2. Ask Initial Questions and Explore the Initiative**

1. The agent MUST ask an explicit initial question set covering:
   - What is the initiative about, and what need or opportunity motivates it?
   - What milestones should the initiative have?
   - What is the current situation or relevant background?
2. The agent MUST adapt the initial question set to the context and MUST omit only questions that are already clearly answered, while using that context to ask relevant follow-up questions instead.
3. The agent MUST then ask targeted follow-up questions for unresolved or ambiguous parts of the initiative.

- The agent SHOULD present answer options when they make a decision clearer, while allowing the user to provide a different answer.

**3. Propose the Initiative Identity**

1. The agent MUST propose an initiative title and its kebab-case variant, even when the user already supplied one.
2. The agent MUST validate the proposed title with the user.
3. The agen must used the validated kebab-case inititative title as a domain.

**4. Propose the Project Charter**

1. The agent MUST propose a concise initiative description.
2. The agent MUST propose additional context relevant to the initiative.

## Output

The job MUST produce a Managed Output containing the validated project charter. Output persistence and the required Context Output are governed by the standard graph-engineering execution rules.

```md
---
title: <initiative title>
domain: <kebab-case domain>
description: <concise initiative description>
---

# <initiative title>

## Description

<validated initiative description>

## Context

<validated context for the user and agent>

## Open Questions

<unresolved questions, when any>
```

## Prompt examples

```txt
Execute the design-job job to design a job named create-initiatives for creating project charters through conversation.
```

```txt
Execute `create-initiatives` job:

Inputs:
- initial idea: I want to build a personal GTD tool.
```