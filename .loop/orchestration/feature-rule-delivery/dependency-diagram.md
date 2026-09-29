# Feature-rule delivery — dependency diagram v2

This flow implements one rule end-to-end. Workers run only after their direct
dependencies complete. Optional workers run only when the delivery boundary
requires their operation class.

```mermaid
flowchart TB
    W1["Worker 1 — Feature Rule Designer"] --> W2["Worker 2 — Capability Researcher"]
    W2 --> W3["Worker 3 — Delivery Boundary Designer"]
    W3 --> W4["Worker 4 — Backend Enabler"]
    W4 --> W5["Worker 5 — Generic Production Service Implementer"]
    W3 --> W6["Worker 6 — Mock Service Implementer"]
    W5 --> W7["Worker 7 — Generic Journey Application Boundary"]
    W6 --> W7
    W3 --> W8["Worker 8 — Named Browser Service Implementer"]
    W8 --> W9["Worker 9 — Named Browser Use Case Composer"]
    W6 --> W9
    W3 --> W10["Worker 10 — Marketplace UI Source Composer"]
    W7 --> W11["Worker 11 — Demo Route Initial-Data Composer"]
    W9 --> W12["Worker 12 — Client Interaction Wire-up"]
    W10 --> W12
    W11 --> W12
    W12 --> W13["Worker 13 — Rule Verification"]
```

## Boundary rules

- Generic server operations follow `service → repository → repository factory → generic use case` and may be exported through the journey use-case barrel.
- Named browser operations follow `named service → named factory in infrastructure/repository → named use case`; their service and use case are imported directly, never through barrels.
- Server initial data belongs in a page or layout. Client hooks own only user-triggered interaction.
- The Marketplace UI receives separate sources and decides its presentation mode; Demo routes transport typed props without choosing UI modes.
