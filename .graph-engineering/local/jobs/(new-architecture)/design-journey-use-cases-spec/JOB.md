# Design Use Cases Specification

## Objective

The job MUST produce an abstract use-case specification for a route or journey by combining visual evidence, current implementation evidence, relevant prior artifacts, and focused design reflection.

The job MUST model the journey as use cases grouped into Server Component Scenarios, Actions Scenarios, Navigation Scenarios, and Local Scenarios.

The job MUST keep the specification independent from literal TypeScript props, database records, repository names, SDKs, and implementation-specific response shapes.

The job MUST NOT audit whether the proposed use cases are implemented correctly. That responsibility belongs to `audit-journey-use-cases`.

## Inputs

The job MUST receive:

- A kebab-case journey identifier;

The job MAY receive:

- An existing specification file to edit in-place;
- At least one visual or descriptive journey reference, such as an image, screenshot, or user description.
- Page, layout, shell, screen, or component paths from the current implementation;
- Relevant source code or workspace paths;
- Prior design, analysis, audit, or reflection artifacts;
- Constraints, naming conventions, or previous design decisions.

Examples:

```txt
Journey: product
Image: C:/path/to/product-journey.png
Page: apps/storefront/src/app/(storefront)/catalog/[slug]/page.tsx
Client: apps/storefront/src/app/(storefront)/catalog/[slug]/product-detail-client.tsx
Artifacts: .graph-engineering/runs/product-journey/
```

```txt
Design the account journey use cases from the supplied screenshot and the account page implementation.
```

## Process

**1. Collect and classify evidence**

1. The agent MUST reuse relevant context, indexes, supplied images, source files, and prior artifacts before discovering additional evidence.
2. The agent MUST inspect the storefront routes related to the requested journey in both the primary storefront route group and the `(demo)` route group when those groups exist.
3. The agent MUST compare analogous routes, layouts, shells, actions, screens, and components across the primary storefront and `(demo)` groups.
4. The agent MUST inspect relevant artifacts under the journey's `.graph-engineering/runs/<journey>/` directory, including previous design, analysis, audit, and reflection outputs.
5. The agent MUST distinguish visual or user-described behavior, behavior observed in the primary storefront, behavior observed in `(demo)`, and behavior proposed by prior artifacts.
6. The agent MUST treat prior artifacts and existing implementation as evidence for design, not as an authoritative contract.

**2. Establish the section plan**

1. The agent MUST prepare the following sections as separate iteration stages:
   - Server Component Scenarios;
   - Actions Scenarios;
   - Navigation Scenarios;
   - Local Scenarios;
   - UI Data Models.
2.1. The Server Component Scenarios section MAY contain a `Common` subsection for server reads and behavior branches executed by a shared layout or route shell. Route subsections MUST contain only scenarios specific to those routes.
2. Before proposing a section, the agent MUST classify internally each scenario candidate as one of: server call, behavior branch, Server Action, navigation, local state transition, or UI rendering detail.
3. The agent MUST preserve the requested section order unless the user explicitly changes it.

**3. Iterate by section with the user**

1. For the current section, the agent MUST propose an initial design based on the collected evidence.
2. Scenario tables MUST default to the columns `Scenario`, `Type`, and `Status`, unless the user requests another schema.
3. Each scenario row MUST keep its title and BDD statements in the `Scenario` cell, using line breaks for `Given`, `When`, and `Then`, using <br/> for line feed. 
4. The `Type` column MUST identify wheter the scenario is a function call, a branch behavior or something else, and `Status` MUST be initially empty unless the user specifies a value.
4.1. Every Server Component scenario classified as a server call MUST identify the function or use-case name that performs the call in its scenario text, such as `getCart` or `getUser`.
5. Server Component Scenarios MUST include server reads and behavior branches that change the route or terminate page preparation. They MUST NOT include client-only context initialization or non-blocking auxiliary failures as a separate scenario unless the user requests that boundary.
6. Actions Scenarios MUST map only to explicit server mutations. Read-only comparisons, snapshot persistence, and other non-blocking auxiliary operations that do not involve a client component MUST remain in the Server Component section when they are invoked there.
7. Navigation Scenarios MUST describe visitor-initiated route changes or any other link behavour like internal scrolling. 
8. Local Scenarios MUST describe only state changes and interactions that do not invoke a Server Action or navigate.
9. UI Data Models MUST begin with the page-facing models and their producers. The agent MUST NOT require DTO-level rows unless the user asks for contracts or the DTO boundary changes the designed behavior.

**4. Add design reflection**

1. After all sections are confirmed, the agent MUST add a concise `Design notes` section containing only cross-cutting rules not already explained under the sections.
2. The agent MUST add a `Focused refinement questions` section with a small number of unresolved questions that could change the final specification.
3. The agent MUST remove questions answered during the section iterations.

**5. Validate the specification**

1. The agent MUST verify that every section reflects the confirmed user decisions.
2. The agent MUST verify that every Actions Scenario maps one-to-one to an explicit server mutation.
3. The agent MUST verify that each scenario is in the section matching its behavior boundary and that UI rendering details were excluded unless requested.
4. The agent MUST verify that scenario rows use the confirmed table schema and include BDD-inspired statements in the `Scenario` cell.
5. The agent MUST verify that every UI Data Model identifies its category, model, and producer, and that any additional contract detail was explicitly requested or necessary to the design.
6. The agent MUST keep the final output abstract and suitable for a later implementation audit.

## Output

The job MUST produce a Managed Output Markdown document containing the specification. If an existing specification file is supplied, the agent MUST edit it in-place, treating it as a Managed Output document as if it were managed by a script.

Output generation and formatting are executed manually by the agent.

The output MUST follow this structure:

```md
# Use Cases - `route`

## Server Component Scenarios

## Actions Scenarios

## Navigation Scenarios

## Local Scenarios

## UI Data Models

## Design notes

## Focused refinement questions
```

Each scenario table MUST use the schema confirmed with the user. Unless changed by the user, it MUST use `Scenario`, `Type`, and `Status`; each Scenario cell MUST contain the title and BDD-inspired `Given`, `When`, and `Then` statements separated by line breaks.
`Type` MUST describe the behavior boundary, such as server call, branch, action, navigation, or local state. `Status` MUST be initially empty unless the user supplies a status.
The UI Data Models section MUST default to `Category`, `Model`, and `Produced by`. It MUST document page-facing models first. DTOs, transport contracts, and mapper details MUST be included only when the user requests them or when they materially constrain the design.
The specification MUST NOT model a rendered notice, loading treatment, disabled control, or other presentation condition as a scenario unless the user explicitly asks for it.

On successful completion, the agent MUST report:

- the journey and evidence analyzed;
- the scenario categories and use cases designed;
- the abstract data-model categories defined;
- the unresolved focused questions;
- the Managed Output file link (or updated in-place specification file path).

On failure, the agent MUST report the missing evidence, unsupported input, or specification-validation error.

## Prompt examples

```txt
Execute the design-use-cases-spec job with:
- Journey: product
- Image: C:/path/to/product-journey.png
- Page: apps/storefront/src/app/(storefront)/catalog/[slug]/page.tsx
- Client: apps/storefront/src/app/(storefront)/catalog/[slug]/product-detail-client.tsx
- Prior artifacts: .graph-engineering/runs/product-journey/
```

```txt
Execute the design-use-cases-spec job using the attached journey image, the supplied route and all relevant prior design artifacts. Produce Server Component, Actions, Navigation, Local, UI Data Models, Design notes, and Focused refinement questions.
```
