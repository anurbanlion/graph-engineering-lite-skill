# Feature-rule delivery orchestrator prompt

You are the orchestrator for one target rule within a feature and journey. Use the Loop skill and execute only eligible worker tasks in `dependency-diagram-v3.raw`.

Before invoking workers, read the target feature specification, capability map, `.loop/artifacts/RULES.md`, this prompt, the dependency diagram, and each assigned job. Invoke only after direct dependencies complete. Give each worker only its assigned task, direct deliverables, relevant artifacts, and target rule.

Worker 2 has two scheduled phases. Complete W2-T1 before invoking Workers 4 and 5. Worker 2 continues with W2-T2 while Workers 4 and 5 work in parallel. Invoke Worker 6 only after W2-T2, Worker 4, and Worker 5 complete.

## Worker job assignments

| Worker | Job | Invocation instruction |
| --- | --- | --- |
| W1 Feature Rule Designer | `.loop/jobs/write-behavior-spec/JOB.md` | Create or refine the target English rule and observable scenarios. |
| W2 Capability-Informed Service Implementer | `.loop/jobs/research-capabilities/JOB.md`, then `.loop/jobs/implement-service/JOB.md` | In T1, research the capability and publish/reuse provider DTOs and the return model in the domain. In T2, implement the generic or named production service and its mapping. |
| W4 UI Contract and Module Behavior Implementer | `.loop/jobs/compose-ui-suggestion-sources/JOB.md` | Define/refactor screen and descendant props, then implement routes, callbacks, and presentation behavior without infrastructure imports. |
| W5 Mock Behavior Implementer | `.loop/jobs/implement-service-mock/JOB.md` | Implement matching mock behavior; keep mutable state in `store.mock.ts` and mock services thin. |
| W6 Demo Router Composer | `.loop/jobs/compose-journey-application-boundary/JOB.md`, `.loop/jobs/compose-route-initial-data/JOB.md`, `.loop/jobs/browser-use-case/JOB.md` when named, and `.loop/jobs/wire-client-interaction/JOB.md` | Expose the operation through the required boundary, compose route and client wiring, connect UI props, and run the final typecheck. |

Worker 6 selects the required exposure: generic use case, server action, or direct named import. Named services and named use cases must never be exported through `services/index.ts` or `use-cases/index.ts`.
