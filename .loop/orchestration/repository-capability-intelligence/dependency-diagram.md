# Repository capability intelligence — dependency diagram

This flow maintains a queryable, evidence-backed repository oracle. Its area is a
domain slice (for example, cart), not a single implementation request. The final
capability map is a global prerequisite for service and data-model work in the
feature-rule-delivery flow.

```mermaid
flowchart TB
    subgraph W1[Worker 1 — Repository Surface Inventory]
        direction TB
        W1A["Inventory relevant paths in apps/storefront, apps/medusa, and packages"]
        W1B["Locate existing routes, APIs, UI contracts, tests, and documentation"]
        W1A --> W1B
    end

    subgraph W2[Worker 2 — Authority and Transport Mapper]
        direction TB
        W2A["Trace request paths, authentication boundaries, and privileged access"]
        W2B["Record the authority for each operation: Storefront API, Medusa, Supabase, or package"]
        W2A --> W2B
    end

    subgraph W3[Worker 3 — Cross-Layer Model Mapper]
        direction TB
        W3A["Trace domain entities, DTOs, front types, schemas, and conversions"]
        W3B["Record source of truth, invariants, and incompatible duplicate models"]
        W3A --> W3B
    end

    subgraph W4[Worker 4 — Legacy Logic and Reuse Mapper]
        direction TB
        W4A["Locate standalone Storefront logic and existing package capabilities"]
        W4B["Classify every candidate as reuse, wrap in apis, migrate, or retire"]
        W4A --> W4B
    end

    subgraph W5[Worker 5 — Repository Oracle Publisher]
        direction TB
        W5A["Reconcile evidence into the domain capability map"]
        W5B["Publish consultation protocol, file pointers, ownership decisions, and open questions"]
        W5A --> W5B
    end

    W1 -->|"surface inventory"| W2
    W1 -->|"surface inventory"| W3
    W1 -->|"surface inventory"| W4
    W2 -->|"authority and transport map"| W5
    W3 -->|"cross-layer model map"| W5
    W4 -->|"reuse and migration decisions"| W5
```

## Deliverable

`.loop/artifacts/capability-map.md`, maintained per domain slice. It is the durable consultation
artifact for all downstream workers; it is not an execution log.
