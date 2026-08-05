# Write Communications

## Objective

The job MUST draft every open communication task from one supplied initiative follow-up while retaining one authored-message history per initiative.

The job MUST NOT send communications, record received replies, or complete source tasks.

## Inputs

The job MUST receive:

- one initiative domain in kebab-case;
- the latest follow-up record for that initiative;
- the latest communication history for that initiative.

The job MAY receive:

- style instruction or feedback.

## Process

1. The agent MUST verify that all inputs belong to the same initiative.
2. The agent MUST extract every open `- [ ] Communication (...)` task from the supplied follow-up record.
3. The agent MUST use the supplied latest communication history as the current authored-message history.
4. The agent MUST ask for missing recipient, purpose, or channel information when it cannot be supported by an open task or Communication Memory.
5. The agent MUST draft every open communication task in the supplied follow-up record.
6. The agent MUST apply user feedback by revising the selected draft or appending the next authored message to its matching thread.
7. The agent MUST resolve the managed-output path for the initiative and write a complete, current history there.

**Recipient Rules**

- The agent MUST identify direct recipients from the selected task or user instruction.
- The agent MUST apply any explicit recipient exclusions or purpose-specific defaults supplied by the user.

**Conventions**

- The agent MUST use the requested channel, language, tone, and signature.
- The agent SHOULD reuse established writing preferences from the latest initiative history when available.

## Output

The job MUST produce a Managed Output: one Markdown communication history per initiative. The latest output MUST preserve all prior authored messages for that initiative.

Output generation and formatting are executed manually by the agent.

```md
# Communication History: <initiative name>

## <email or message thread title>

### DD/MM/YYYY — <channel> draft
**To:** <direct recipients>
**CC:** <copy recipients or —>
**Subject:** <subject when email>

<message authored by the user>
```

Each `##` heading MUST be one email or message thread title. A new authored message MUST be appended to its matching thread; a new thread MUST be created only when none matches. The output MUST NOT include Communication Memory, feedback-pending sections, received replies, or task-status changes.

On successful completion, the agent MUST report:

- drafted communication tasks and initiative domain;
- generated history file links.

On failure, the agent MUST report the missing selection, recipient, purpose, channel, or output-generation error.

## Prompt examples

```txt
Execute draft-initiative-communications and show me the open communication tasks.
```

```txt
Draft the email for the New Web Guidelines SEO decision task in a concise Spanish tone.
```
