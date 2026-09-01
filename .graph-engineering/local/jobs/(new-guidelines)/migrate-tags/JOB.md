# Migrate Tags

> Version: 1.0

## Objective

The job MUST accept a target page and forward that page unchanged as the initial handoff for future tag application work.

The job MUST NOT inspect, create, modify, or remove page files, tags, or any other project output.

## Inputs

The job MUST receive:

- A page identifier or page file path to which new tags will eventually apply.

Examples:

```txt
apps/storefront/src/app/[lang]/account/page.tsx
```

## Process

1. The agent MUST verify that a page identifier or page file path was supplied.
2. The agent MUST forward the supplied value unchanged as structured standard output with the field `page`.
3. The agent MUST NOT perform any tag application work during this version of the job.

## Output

The job MUST produce no project output and MUST emit structured standard output.

```json
{
  "page": "<supplied-page-identifier-or-path>"
}
```

On successful completion, the agent MUST report the forwarded page value and that no tags were changed.

On failure, the agent MUST report that the page input is missing.

## Prompt examples

```txt
Execute the migrate-tags job for apps/storefront/src/app/[lang]/account/page.tsx.
```

```txt
Run migrate-tags for the checkout page.
```
