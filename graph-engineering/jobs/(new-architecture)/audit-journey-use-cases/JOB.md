# Audit Journey Use Cases

## Objective

The job MUST perform a deep audit of every use case identified during the design phase against the actual backend and package landscape.

The job MUST produce a **Blueprint** document that serves as the single source of truth for all downstream implementation jobs.

The job MUST reconcile the preliminary UI data models with backend boundaries, recommending use case decomposition or model adjustments when the audit reveals misalignments.

## Inputs

The job MUST receive:

- A kebab-case journey identifier;
- The design-use-cases artifact for the journey (available in context via Echo mode).

## Scope

The agent MAY inspect:

```txt
apps/storefront/
apps/medusa/
packages/
supabase/migrations/
```

## Process

**1. Five-Layer Discovery**

For each use case identified in the design artifact, the agent MUST audit these layers:

1. **Medusa Endpoints**: Store REST routes, custom plugin routes, or admin routes that serve the required data or mutation.
2. **Supabase Auth**: `auth.getUser()`, `auth.updateUser()`, or other Auth SDK operations.
3. **Supabase DB Tables**: Direct table queries via the Supabase client (inspect migrations for schema).
4. **Package SDKs**: Functions exported by `packages/*` that wrap or orchestrate backend calls.
5. **Storefront Implementations**: Existing server actions, demo functions, in-memory stores, or custom wrappers in the Storefront app.

**2. Reconcile UI Models with Backend Boundaries**

1. The agent MUST compare each preliminary UI data model against the discovered backend sources.
2. When a single UI model requires data from multiple disjoint sources (e.g. Auth user + `user_profiles` table + `customer_addresses` table), the agent MUST recommend whether to split the model into separate types or keep a unified type with multi-source assembly.
3. When the audit reveals that a single use case should be decomposed into multiple granular operations (e.g. `getUser` → `getCurrentUser` + `getDeliveryAddresses`), the agent MUST document the recommended decomposition and its rationale.

**3. Document Field Mappings and Service Specs**

1. For each use case requiring data adaptation, the agent MUST produce a field mapping table comparing backend source fields to UI model fields.
2. The agent MUST classify each mapping: Direct, Conditional, Backend-only, UI-only, or Unverifiable.

**5. Reflection (Stabilization Check)**

This section MUST be produced independently from the audit and placed at the end of the Blueprint document.

The agent MUST answer the following questions explicitly:

1. **Data sourcing**: For each UI data model, can the required fields be obtained from the discovered backend sources? Are there gaps or unverifiable fields?
2. **Model optimality**: Is the proposed UI data model structure optimal given the backend boundaries? Should any model be split into separate types to avoid joining disjoint sources in a single call? Should any models be merged because they share the same source?
3. **Use case alignment**: If models are split or merged, do the current use case signatures still make sense? Should any use case be decomposed or consolidated?

The agent MUST produce a clear verdict: `STABLE` or `REQUIRES_REFINEMENT`.

When `REQUIRES_REFINEMENT`, the agent MUST list the specific changes needed (e.g. "Split `User` into `UserProfile` and `DeliveryAddress[]`; decompose `getUser` into `getCurrentUser` + `getDeliveryAddresses`").

When `STABLE`, the agent MUST present the final Blueprint to the user for approval before proceeding.

## Output

The job MUST produce a Managed Output (Blueprint) as a Markdown document with the following structure:

```md
# <Journey> Journey Blueprint

## Reconciled Use Cases

| Use Case | Preliminary | Final | Rationale |
| --- | --- | --- | --- |
| `getUser` | Single operation returning `User` with addresses | Split into `getCurrentUser` + `getDeliveryAddresses` | Auth user and addresses come from disjoint sources. |

## Reconciled UI Data Models

| Model | Fields | Changes from Preliminary | Notes |
| --- | --- | --- | --- |
| `User` | `name`, `email`, `phone` | Removed `addresses` (separate query) | Auth + `user_profiles` table. |
| `DeliveryAddress` | `addressLine1`, `city`, `isDefault` | Added `isDefault` from backend | `customer_addresses` table. |

## Five-Layer Discovery Matrix

### Use Case: `getCurrentUser`

| Layer | Status | Source / Reference | Notes |
| --- | --- | --- | --- |
| Medusa Endpoint | ❌ None | — | No custom endpoint. |
| Supabase Auth | ✅ Available | `auth.getUser()` | Returns `id`, `email`. |
| Supabase DB | ✅ Available | `user_profiles` table | `display_name`, `phone`. |
| Package SDK | ✅ Available | `@chiki/account-sdk` → `getCurrentUser()` | Wraps Auth + profile query. |
| Storefront | 🟡 Mock | `getCurrentUser()` in `server-db` | In-memory mock store. |

## Field Mapping Specifications

### `getCurrentUser` → `User`

| Backend Source | UI Model Field | Mapping |
| --- | --- | --- |
| `auth.user.email` | `email` | Direct |
| `user_profiles.display_name` | `name` | Direct |
| `user_profiles.phone` | `phone` | Direct when present |
| `user_profiles.avatar_url` | `avatarUrl` | Direct |
| — | `mapThumbnail` | No verified backend source |

## Data Flow Diagram

(Mermaid graph TB diagram)

## Reflection

- **Data sourcing**: All fields for `User` are available via Auth + `user_profiles`. Addresses require a separate `customer_addresses` query.
- **Model optimality**: `User` should NOT include addresses because they come from a disjoint table. Splitting is recommended.
- **Use case alignment**: `getUser` should be decomposed into `getCurrentUser` + `getDeliveryAddresses`.
- **Verdict**: `REQUIRES_REFINEMENT` | Changes: Split `User` model, decompose `getUser` use case.
```

On successful completion, the agent MUST report the use cases audited, models reconciled, decomposition changes, the reflection verdict, and the managed output file link.

## Prompt examples

```txt
Execute the audit-journey-use-cases job for the account journey.
```

