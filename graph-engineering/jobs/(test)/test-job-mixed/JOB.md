# Test Job Mixed

> Version: 1.0
> Location: `graph-engineering/jobs/test-job-mixed/JOB.md`

## Objective

The job MUST generate a structured product specification sheet for a given product or device, detailing key specifications, advantages, trade-offs, and target user profile.

## Inputs

The job MUST receive:

- `product_name`: Name or model identifier of the target product;
- `domain`: A kebab-case domain identifier.

The job MAY receive:

- `category`: Product category (e.g., `laptops`, `smartphones`, `audio`);
- `budget_tier`: Price or market tier segment (e.g., `entry`, `midrange`, `flagship`).

Examples:

```txt
Execute the test-job-mixed job with product_name="Laptop Pro 14" and domain="laptops".
```

```txt
Execute test-job-mixed for product_name="Wireless Headphones ANC" domain="audio" category="audio" budget_tier="midrange".
```

## Process

1. The agent MUST use only its knowledge and and organize key specifications, advantages, trade-offs, and target user profile for the product.

## Output

The job MUST produce a Managed Output as a Markdown document containing the product specification sheet.

**Markdown Document Output**

```md
# Product Specification Sheet: <product_name>

## Overview

- **Product Name**: <product_name>
- **Category**: <category>
- **Tier**: <budget_tier>

## Key Specifications

- **Performance**: <spec-summary>
- **Build & Design**: <build-summary>
- **Battery & Connectivity**: <battery-summary>

## Assessment

- **Pros**: <pros-list>
- **Cons**: <cons-list>
- **Target Audience**: <target-audience>
```

**Context Output Extension**

In addition to the mandatory links for generated artifacts, the Context Output MUST report:

- **Summary**: Key technical specifications summary and overall rating;
- **Top Feature**: Most notable feature or core strength;

## Prompt examples

```txt
Execute the test-job-mixed job with product_name="Laptop Pro 14" and domain="laptops".
```

```txt
Execute the test-job-mixed job in two sequential steps:
1. Load its definition into context by running `design-job` in Latest mode with domain test-job-mixed.
2. Immediately proceed to execute test-job-mixed in Default mode using the loaded process.

Inputs for test-job-mixed job:
- product_name: "Laptop Pro 14"
- domain: "laptops"
- category: "laptops"
- budget_tier: "flagship"
```
