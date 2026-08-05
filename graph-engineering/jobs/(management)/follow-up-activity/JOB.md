# Follow-up Activity

## Objective

The job MUST transform meeting notes, status updates, or free-form initiative context into a concise follow-up record for one initiative.

## Inputs

The job MUST receive:

- a kebab-case domain identifier representing exactly one initiative;
- source context or text containing one or more meeting notes, updates, decisions, or action items;

The job MAY receive:

- a date in `DD/MM/YYYY` format for each source event, or one shared date for all provided events.
- an existing follow-up record for the same initiative;
- a compiled organization context containing known people, areas, roles, responsibilities, systems, or relationships;
- default owners, deadlines, or naming conventions.

Examples:

```txt
domain: metodo-de-testeo
context: En la reunion se redefinio el alcance de unit testing hacia la propuesta de un metodo de testeo. Debo enviar el correo de formalizacion.
```

```txt
domain: landing-educacion-financiera
context: Brenda hablara con Renato. Antes de ofrecer una alternativa, Brand debe confirmar si la iniciativa se ejecutara este trimestre.
```
## Process

**1. Validate initiative context**

1. The agent MUST confirm that the domain is a non-empty kebab-case identifier for one initiative.
2. The agent MUST request a domain when it is absent.
3. The agent MUST request source context when no notes or status update are provided.
4. The agent MUST identify the current date when it is absent and use `DD/MM/YYYY` format.

**2. Extract Events and Agreements**

1. The agent MUST extract an event only when the source identifies an occurrence, meeting or an agreement in a meeting.
2. The agent MUST record only agreements that are explicit in the source.
3. The agent MUST preserve the relationship between an agreement and its originating event.

Example:

```txt
Source: En la reunión con Brenda, Rafael y César acordaron que Brenda hablará con Renato.
Result:
- 03/08/2026 Reunión con Brenda, Rafael y César sobre la viabilidad de la iniciativa.
  - Acuerdo: Brenda conversará con Renato para validar la viabilidad de la iniciativa.
```

```txt
Source: Renato le dijo a Brenda que debíamos pensar en una alternativa a la landing en caso no se ejecute.
Result:
- 03/08/2026 Renato solicitó a Brenda encontrar una alternativa a la landing en caso de que no se ejecute.
```

**3. Extract Tasks**

1. The agent MUST extract explicit commitments, assigned actions, and requested actions as tasks, preserving the stated owner or leaving it unassigned.
2. The agent SHOULD create tasks that operationalize an agreement and MAY split broad agreements into smaller actionable tasks when this improves execution clarity.
3. The agent MUST classify every request to write or send an email or a message as a single, standalone communication task.
4. The agent MUST place a possible action in `Suggestions` when the source does not support it as a task.

Example:

```txt
Source: En la reunión, Rafael acordó actualizar el Excel de actividades.
Result: Create a task for Rafael to update the Excel of activities.
```

**4. Extract Additional and Organization Context**

1. The agent MUST extract strategy definitions, scope criteria, constraints, and implementation aspects as `Additional Context`.
2. The agent MUST consolidate related strategy elements into one cohesive statement when they describe the same strategy.
3. The agent MUST record `Organization Context` as independent, atomic, and reusable organizational facts.
4. The agent MUST record organization information only when it is explicit in the source or is a directly supported inference.
5. The agent MUST NOT include meeting participation, temporary task ownership, initiative-specific commitments, or inferred responsibilities as organizational facts.
6. When a compiled organization context is provided, the agent MUST use it as the baseline for organization facts.
7. When a compiled organization context is provided, the agent MUST NOT repeat an equivalent known fact in `Organization Context`.
8. When a source explicitly contradicts a known organization fact, the agent MUST add one atomic `Contradiction:` entry that states both values and MUST NOT choose either value.
9. When no compiled organization context is provided, the agent MUST treat every supported organization fact as new.

Examples:

```txt
Source: La estrategia debe definir la librería y los tipos de prueba.
Result: Add one cohesive strategy statement to Additional Context.

Source: Will pertenece a Arquitectura Frontend.
Result: Add the atomic fact "Will pertenece al área de Arquitectura Frontend." to Organization Context.

Source: Rafael debe actualizar el Excel de actividades.
Result: Add the task to Tasks and the atomic fact "Existe un archivo Excel donde se organizan las tareas." to Organization Context.
```

```txt
Compiled context: Will pertenece a Arquitectura Frontend.
Source: Will pertenece a Arquitectura Frontend.
Result: Do not repeat the fact in Organization Context.
```

```txt
Compiled context: Will pertenece a Arquitectura Frontend.
Source: Will pertenece a Ingeniería.
Result: Add "Contradiction: Will pertenece a Ingeniería; the compiled organization context states that Will belongs to Arquitectura Frontend." to Organization Context.
```

**5. Derive Suggestions**

1. The agent MUST derive suggestions only from known tasks, dependencies, missing information, dates, commitments, or organization context.
2. The agent MUST NOT turn a suggestion into a task unless the source explicitly assigns it.
3. The agent MUST omit speculative suggestions when the available information does not support an actionable recommendation.

Example:

```txt
Source: La estrategia requiere la aprobación de Will y Jeff, pero no define criterios de aprobación.
Result: Suggest confirming the approval criteria; do not create a task unless the source assigns it.
```

## Output

The job MUST produce a Managed Output: one persisted Markdown follow-up record for the supplied initiative domain.

Output generation and formatting are executed manually by the agent.

```md
<!-- Keep fixed Markdown structure in English. Write all initiative content in Spanish. Remove these comments before saving the managed output. -->
# Follow-up: <initiative name>

## Events

<!-- Every first-level event MUST begin with DD/MM/YYYY.
When the source provides only a partial date, preserve the unknown component using ?:
??/MM/YYYY or ??/??/YYYY. Use the applicable format below. -->

<!-- Meeting event format. -->
- DD/MM/YYYY Reunión con [personas y/o squad] sobre [tema o temas]
  - Acuerdo: <acuerdo>

<!-- Other confirmed event format, such as a request, planning activity, or decision. -->
- DD/MM/YYYY <persona o área> <acción o hecho verificable>.

<!-- Partially dated confirmed event format. -->
- ??/MM/YYYY <persona o área> <acción o hecho verificable>.

## Tasks

<!-- Use checkbox tasks and an owner whenever known. Retain open tasks unless there is explicit completion evidence. -->
- [ ] (<responsable>): <acción concreta>
<!-- Keep each communication task isolated. It MUST name one action, channel (correo | mensaje), recipient, and purpose. Do not draft the communication itself. -->
- [ ] Communication (<responsable>): Enviar un <canal> a <destinatarios> sobre <propósito>.

## Additional Context

<!-- Express strategy definitions, constraints, and scope as cohesive statements, never as task checkboxes. -->
- <definición estratégica o aspecto de alcance expresado como una idea cohesiva>

## Organization Context

<!-- When no compiled organization context is supplied, build a simple reusable organizational memory as a flat list of independent atomic facts. When one is supplied, include only new facts or explicit contradictions. Do not include temporary tasks, meeting participation, initiative-specific commitments, or inferred responsibilities. -->
- <hecho organizacional atómico y sustentado>
- <person is known to exist>
- <person belongs to a known area>
- <known shared file, list, or system>
- <explicit stable relationship between people, areas, or artifacts>
- Contradiction: <source fact> conflicts with <known organization fact>

## Suggestions

<!-- Keep suggestions brief when organizational context, activities, or dates are incomplete. Base them only on available information. -->
- <sugerencia sustentada en la información disponible>
```

On successful completion, the agent MUST report:

- the initiative domain used;
- the managed-output file link;
- a concise summary of added facts, open tasks, and decisions.

On failure, the agent MUST report the missing or invalid domain, missing context, or output-generation error.

## Prompt examples

```txt
Execute follow-up-activity job for the metodo-de-testeo domain with date 03/08/2026 and these notes: ...
```

```txt
Execute follow-up-activity job twice, one in latest mode and the next one on default. If latest mode does not return an output, ignore it and create a file without previous events, do this for the domain:

- metodo-de-testeo

and these notes:
```

```txt
Update landing-educacion-financiera with the 03/08/2026 meeting notes: ...
```
