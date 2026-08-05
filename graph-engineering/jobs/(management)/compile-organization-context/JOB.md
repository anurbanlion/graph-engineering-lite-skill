# Compile Organization Context

## Objective

The job MUST consolidate precompiled organization facts into one current Markdown organization context covering areas, people, roles, responsibilities, and supported relationships.

The job MUST NOT inspect follow-up artifacts, discover project files, or invent organization facts.

## Inputs

The job MUST receive:

- a kebab-case domain identifier for the managed output;
- one or more prepared organization context documents.

The job MAY receive:

- an existing organization context for the same domain;
- explicit corrections or conflict-resolution decisions;
- formatting or language preferences.

Examples:

```txt
domain: global-info
sources:
- prepared organization context documents
```

## Process

**1. Validate Sources**

1. The agent MUST confirm that the domain is a non-empty kebab-case identifier.
2. The agent MUST request at least one prepared source document when none is supplied.
3. The agent MUST treat an existing organization context as additional input, not as an unquestioned authority.

**2. Normalize Facts**

1. The agent MUST extract only explicit facts about areas, people, email addresses, roles, responsibilities, memberships, and stable relationships.
2. The agent MUST normalize repeated references to the same person or area when the available names clearly identify the same entity.
3. The agent MUST NOT infer a role, area membership, reporting relationship, or responsibility from temporary task ownership or meeting participation.

**3. Reconcile Conflicts**

1. The agent MUST merge equivalent facts.
2. The agent MUST apply an explicit user correction over conflicting source facts.
3. The agent MUST list unresolved contradictions in a `## Conflicts` section and MUST NOT silently choose one value.

**4. Write Context**

1. The agent MUST resolve the managed-output path using the supplied domain and `compile-organization-context` job name.
2. The agent MUST write a complete current context document to the resolved path.
3. The agent MUST organize confirmed people under their known area headings.
4. The agent MUST list people without a confirmed area in `## Unassigned People`.
5. The agent MUST record each area responsibility as a separate nested list item.
6. The agent MUST include empty sections when no supported facts exist for them.

## Output

The job MUST produce a Managed Output: one Markdown organization context for the supplied domain.

Output generation and formatting are executed manually by the agent.

```md
# Organization Context

## Areas

### <area>

- Responsibilities:
  - <area responsibility or —>
- Members:
  - <person>
    - Emails:
      - <email address or —>
    - Role: <role or —>
    - Responsibilities:
      - <person responsibility or —>

## Unassigned People

- <person>
  - Emails:
    - <email address or —>
  - Role: <role or —>
  - Responsibilities:
    - <person responsibility or —>

## Relationships

- <supported relationship>

## Conflicts

- <unresolved contradiction or None>
```

On successful completion, the agent MUST report:

- the managed-output file link;
- the areas, people, and relationships consolidated;
- unresolved conflicts, if any.

On failure, the agent MUST report the missing domain, missing prepared sources, or unresolved input ambiguity.

## Prompt examples

```txt
Compile an organization context for the ntt-management domain from these prepared organization fact documents.
```

```txt
Update the ntt-management organization context with these new prepared facts and preserve unresolved contradictions.
```
