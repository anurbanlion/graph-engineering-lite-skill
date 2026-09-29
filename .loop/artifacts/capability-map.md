# Repository Oracle — capability map

## Decision rules

| Need | Owner / import path | Decision |
| --- | --- | --- |
| HTTP transport and structured result handling | `@chiki/medusa-client` | Reuse. Add generic transport behavior there only when it is useful beyond cart. |
| Storefront server session and JWT forwarding | `@chiki/supabase/server` | Reuse on server only. Forward the session token to Medusa; do not use privileged Supabase access in Storefront cart code. |
| Privileged listing, saved-item, and buyer-cart persistence | `apps/medusa` marketplace routes plus `req.supabaseAdmin` | Medusa owns it. Storefront must call the marketplace route, not Supabase directly. |
| Cart workflows and cart ownership | `apps/medusa/src/api/marketplace/_lib` and marketplace routes | Medusa owns it. Reuse the existing cart route surface before creating another backend path. |
| Storefront-facing cart operations | `apps/storefront/apis/cart` | The target façade. It owns front-facing contracts, mapping, use cases, actions, repository selection, and mock/prod parity. |
| Existing pre-`apis` cart wrappers | `apps/storefront/src/lib/marketplace-cart.ts`, `marketplace-save-for-later.ts`, `cart-presentation.ts` | Treat as migration candidates: extract or wrap their reusable transport and presentation logic into `apis/cart`; do not duplicate their behavior. |
| UI screens and front types | `@chiki/ui/marketplace-v2` | Reuse as presentation contracts. It must not import Storefront APIs, Medusa, or Supabase. |

## Known cart capability paths

| Behavior capability | Storefront entry | Medusa authority |
| --- | --- | --- |
| Read owned cart | `getCartSnapshot()` in `apis/cart` | `GET /marketplace/cart`, then cart reconciliation/presentation mapping |
| Change line quantity | cart action → repository/service | `PATCH /marketplace/cart/items/:lineId`; validates ownership, availability and stock |
| Remove line | cart action → repository/service | `DELETE /marketplace/cart/items/:lineId`; idempotent deletion |
| Save line for later | cart action → repository/service | `POST /marketplace/cart/items/:lineId/save-for-later` |
| Read saved items | `getSavedItemsSnapshot()` in `apis/cart` | `GET /marketplace/save-for-later` plus presentation lookup |
| Restore saved item | cart action → repository/service | `POST /marketplace/save-for-later/:listingId/move-to-cart` |
| Remove saved item | cart action → repository/service | `DELETE /marketplace/save-for-later/:listingId` |
| Fulfillment choices | `getFulfillmentOptions()` in `apis/cart` | `GET /marketplace/checkout/fulfillment-options` |

## Search capability assessment — initial suggestions

### Rule assessed: `When search starts, popular suggestions are displayed`

The rule needs two independent, initial (empty-query) sources: at most two popular
search queries and at most two popular products. It is satisfied only when both
successful source reads are empty; an unavailable source is not evidence that no
popular suggestion exists.

### Existing capabilities and authority

| Need | Evidence | Owner and call boundary | Decision |
| --- | --- | --- | --- |
| Popular search queries | `supabase/migrations/20260708030000_analytics_date_range.sql` defines `get_search_trends(p_store_id, p_days, p_limit, p_from, p_to)`. Its `top_queries` are normalized queries, ranked by count, and the function allows only `service_role`; it clamps `p_limit` to `1..100`. | Supabase analytics capability; a trusted Storefront server service may call it with `createAdminClient()` from `@chiki/supabase/admin`. Never expose that client or RPC to the browser. Existing Medusa consumers at `apps/medusa/src/api/marketplace/admin/trends/route.ts` and `apps/medusa/src/api/marketplace/stores/[storeId]/trends/route.ts` are privileged analytics routes, not buyer endpoints. | Reuse the RPC server-side with `p_store_id: null`, `p_days: 7` (its default window), and `p_limit: 2`; project only `top_queries[].query` into popular-search suggestions. |
| Popular product rows | `packages/search/src/discovery.ts` exposes `listCatalogBestsellers(client, { limit })`; it calls public `list_catalog_bestsellers`. `supabase/migrations/20260713191000_catalog_bestsellers.sql` limits that RPC to `1..24`, exposes only PII-free catalog display data, and ranks paid online sales from 30 days with a duplicate-free 90-day fallback. | `@chiki/search` discovery capability; public Supabase RPC, callable with the server session client or a browser client. `apps/storefront/apis/home/infrastructure/services/home.service.ts` is an existing server-side mapping reference. | Reuse it in the initial-suggestions server service with `limit: 2`. Map only the fields required by the delivery contract rather than carrying Home's grid model. |
| Search telemetry that feeds trends | `supabase/migrations/20260627080000_search_analytics_init.sql` defines locked `search_query_log` and the public, security-definer `log_search_query`; `packages/search/src/catalog.ts` calls it after a successful first-page `searchCatalog` when `logAnalytics` is set. | Query writes are public best-effort telemetry; trend reads remain service-role only. | Reuse as the popularity data source; do not write on focus or autocomplete. Only confirmed text searches feed this source. |
| Initial-popular service boundary | `apps/storefront/apis/catalog` currently has a browser-safe named autocomplete service; `apps/storefront/apis/search` has server-only `search.service.ts`; neither exposes popular initial suggestions. | Storefront API server boundary. The browser-safe autocomplete chain cannot import `@chiki/supabase/admin`. | Create a separate server-only initial-suggestions service/use case in `apps/storefront/apis/catalog`; it composes the two source reads and passes a safe delivery model to the demo server route/layout. Do not add privileged reads to `auto-complete.service.ts`. |
| Current UI contract | `packages/ui/src/marketplace-v2/types/catalog.types.ts` already represents `kind: "hot"` and `kind: "product"`; `SearchAutocomplete.tsx` has presentation rows for `hot` and products. | UI owns display types and rows; it must not import Storefront APIs or Supabase. | The later delivery-contract worker should specify the exact popular-product row fields and ensure the initial payload reaches this UI contract. |
| Empty popular condition | `listCatalogBestsellers` returns `{ results: [], error: null }` for an honest empty result; `get_search_trends` returns `top_queries: []` when its aggregate has none. Both return distinct error values on failure. | Storefront service owns composition and error distinction. | Return no popular suggestions only when both reads are successful and empty. Preserve an explicit error outcome if either source fails; do not silently render that failure as the BDD's empty condition. |

### Rule-specific recommendation

1. Create one **server-only** initial-popular-suggestions operation under the Catalog API journey. It MUST run the two independent reads in parallel: `get_search_trends(..., p_limit: 2)` through `createAdminClient()` and `listCatalogBestsellers(..., { limit: 2 })`.
2. Project trend rows to at most two `hot` suggestions and bestseller rows to at most two `product` suggestions. The delivery-contract worker decides the minimum product fields, but the existing UI model currently needs `title`, `slug`, and `game` for a product row.
3. The Demo server layout/page SHOULD invoke that server operation on initial render and pass its UI-ready result down. The client autocomplete hook remains responsible only for non-empty typed queries.
4. Treat source errors separately from empty data. The current rule defines the no-popular state, not an outage state; error display/fallback behavior is an unresolved delivery-contract decision.
5. Do not use the existing Medusa trends routes for this buyer feature: their authorization requires platform-admin or store membership and their payload is analytics-oriented.

### Open decisions and gaps

| Gap | Evidence | Required decision before implementation |
| --- | --- | --- |
| Trend eligibility | `get_search_trends` includes top queries that may have `no_results: true`; the BDD does not say whether failed searches are allowed as popular suggestions. | Decide whether to show all popular queries (current source behavior) or filter no-result trends. Filtering needs either a Storefront projection rule or a new dedicated RPC. |
| Trend window | The current aggregate defaults to seven days; the BDD specifies no time window. | Confirm the seven-day default or specify another product window before the service contract is finalized. |
| Failure presentation | Both source APIs expose errors, but the UI's current initial state only distinguishes suggestions from absence. | Define loading/error behavior so a backend outage is not rendered as “no popular suggestions.” |
| Rule coverage | The spec's popular rule currently names a scenario for popular searches but not a separate scenario for popular products, while the intended behavior requires both sources. | Add or refine the product scenario in the BDD before verification. |

### Search capability summary

| Behavior | Existing capability | Proposed implementation |
| --- | --- | --- |
| Search the catalog when confirmed | `searchCatalog` from `@chiki/search` | Call it from server `apis/search` with `logAnalytics`; it searches and records the query automatically. |
| Show matches while typing | `autocompleteCatalog` from `@chiki/search` | Call it through the browser-safe Catalog named service with debounce; it does not record history or analytics. |
| Record a search | `log_search_query` and Supabase `search_query_log` | This happens after a successful non-empty confirmed search; selecting a suggestion does not record a query. |
| Show popular searches | `get_search_trends` over `search_query_log` | Use `createAdminClient()` only in a server-only Catalog initial-suggestions service; request and project at most two queries. |
| Show popular products | `listCatalogBestsellers` from `@chiki/search` | Call it in that server-only service with `limit: 2`; project at most two product rows. |
| Show recent history | `search_query_log` contains `user_id`, query, and timestamp | Deferred to its own rule: add a server-only authenticated-user read with an explicit privacy decision. |
| Compose initial suggestions | No unified operation exists | Compose independent popular-query and popular-product results; add history only when its own rule is delivered. |
| Show an empty state | `SearchAutocomplete` already owns no-suggestion presentation | Render the empty condition only when the composed sources successfully return no popular entries. |

Only confirmed text searches are recorded as search history. Selecting a product or
any other suggestion does not record a search query and does not add an entry to
recent history.

## Product-detail capability assessment — canonical information and navigation

### Rule assessed: `A product detail displays its canonical product information`

The current scope is read-only product information and navigation. Adding an item
to cart and buying now are deliberately excluded. Seller listings and
Chiki-Elección are useful adjacent capabilities, but do not define the canonical
product itself.

### Existing capabilities and authority

| Need | Evidence | Owner and call boundary | Decision |
| --- | --- | --- | --- |
| Read a public canonical product | `apps/storefront/apis/product/infrastructure/services/product.service.ts#getProduct` reads `canonical_catalog_items`, `games`, `expansion_sets`, `catalog_media`, and the matching subtype table. The existing non-demo route `apps/storefront/src/app/catalog/[slug]/page.tsx` performs the same aggregate read. | Storefront server-side Product API; use the server Supabase client so public RLS determines visibility. | Reuse `getProduct` as the primary capability. It already returns title, item type, game, nullable expansion, ordered media, and subtype details. |
| Product image and display metadata | `catalog_media` carries `storage_path`, `alt_text`, `is_primary`, and `sort_order`; the existing page maps it with `catalogImageUrl` and selects primary media first. | Canonical catalog storage, mapped by the Product API. | Reuse the existing deterministic media mapping. A missing media row is a valid presentation fallback, not a reason to fail the product read. |
| Card, sealed-product, and accessory information | `canonical_card_details`, `canonical_sealed_product_details`, and `canonical_accessory_details` are mutually constrained 1:1 subtypes. The Product API returns the discriminated `ProductDetails` model. | Canonical catalog schema and Product API. | Reuse the discriminated detail model. Card-only fields must not be required for sealed products or accessories. |
| Card legality | The catalog migration has no first-class legality table or column. The existing UI merely renders a `Legalidad de Carta` tab; no Storefront, Medusa, migration, or `@chiki/search` capability supplies typed legality data. Card details retain only untyped `game_specific_attributes`. | No confirmed authoritative capability. | Treat legality as a gap. It can only be displayed when a future, explicitly typed card-legality model/source is introduced; do not infer it from the current free-form attributes. |
| Active/not-found visibility | Public catalog RLS uses `is_public_catalog_item`; the non-demo route treats an RLS-hidden or absent CCI as `notFound()`. A CCI may have no expansion because `expansion_set_id` is nullable. | Supabase RLS plus canonical catalog schema. | Preserve this behavior: inactive/hidden/missing products resolve to not found; an active product without an expansion remains displayable and has no expansion destination. |
| Chiki-Elección | `@chiki/search#getCatalogListingRecommendation` calls `resolve_catalog_listing_recommendation`; the resolver chooses an eligible seller listing via a manual HQ override or the cheapest eligible listing. `apps/medusa/.../admin/chiki-choice/[catalogItemId]/route.ts` manages that override. | Listing recommendation capability, not canonical product data. | Keep it outside the first canonical-information rule. It becomes relevant only with the seller-listings rule / featured listing presentation. |
| Available seller listings | `getActiveListingsForCci` and the existing Product API expose `sellerListings`; the legacy route maps them to the listing section. | Storefront listing helper / seller-listing persistence. | Reuse for the later listings rule, not as a prerequisite for canonical product rendering. |
| Product detail endpoint in Medusa | `apps/medusa/src/api` has seller, admin, cart, checkout, and catalog-request endpoints, but no buyer-facing canonical product-detail endpoint. | No Medusa buyer-read capability exists for this aggregate. | Do not add a Medusa hop merely to read the public CCI. The Product API's server Supabase read is the established implementation. |

### Navigation capability assessment

| Destination shown in the reference | Existing behavior | Decision / limitation |
| --- | --- | --- |
| Game catalog | Search supports `gameSlug`; the non-demo detail page already has the item's game slug. | Route to the catalog filtered by game. This is supported. |
| Expansion catalog | Search supports `gameSlug` and `expansionSlug`; the non-demo detail page builds `/catalog?game=<game>&expansion=<expansion>` only when both exist. | Reuse this guarded route. Do not render/enable it without an expansion. |
| Other prints | The non-demo route currently builds `/catalog?q=<product title>`. The schema has an optional `card_print_groups` relation for reprints/variants, but `getProduct` does not return it and `searchCatalog` exposes no print-group filter. | The existing title search is only a fallback approximation. A correct print relation needs a Product API field for the group and a search/filter capability keyed by it (or a dedicated related-prints operation). |
| Other listings | The non-demo client's `onViewOtherListings` scrolls to its local seller-listings section; it does not navigate elsewhere. | Reuse as in-page navigation when the later listings rule is implemented. It is unavailable until that section is present. |
| Seller profile | Seller listings expose store identity, and `@chiki/search` exposes `getPublicStoreProfile` / `listPublicStoreCatalog`; no current Product Detail client wires a seller-profile link. | The data capability exists, but the storefront route contract still needs to define the public seller URL before this rule is implemented. |
| Sell this card | `ProductDetailScreen` has an optional `onSellThisCard` presentation callback, but the non-demo client never supplies it. Medusa exposes a seller-only catalog-request flow, not a buyer-facing product-detail sell destination. | No current navigation capability. Keep it out of the read-only delivery scope until the seller-entry route and eligibility are defined. |

### `@chiki/search` boundary

`@chiki/search` supplies catalog search/autocomplete, public discovery, and the
buyer-safe Chiki-Elección listing recommendation. It does **not** expose a
canonical-product detail read, card legality, or related-prints operation. The
canonical product aggregate remains a Storefront server read over the catalog
tables.

### Required follow-up decisions before implementation

1. Keep the existing `ProductPage` aggregate as the service return model, or move
   that shared read model into the UI domain before the new feature reuses it.
2. Define a typed legality source before promising the `Legalidad de Carta` tab;
   current data is insufficient for a reliable rule.
3. Decide whether `Otros prints` may remain title-search fallback temporarily. If
   not, add a print-group-aware read/filter capability first.
4. Define the public seller-profile route before wiring seller navigation. Do not
   use the seller-only Medusa catalog-request endpoint as its substitute.

## Product-detail capability assessment — seller listings and Chiki-Elección

### Rules assessed

- `A product detail displays its available seller listings`
- `The user can order available seller listings`

### Existing capabilities and authority

| Need | Evidence | Owner and call boundary | Decision |
| --- | --- | --- | --- |
| Read active listings for one canonical product | `apps/storefront/src/lib/listings.ts#getActiveListingsForCci` uses the server Supabase client to read public `seller_listings` joined to `stores`. The migration grants read access only to active listings whose parent CCI is public. | Existing Storefront server helper over RLS-protected Supabase. There is no buyer-facing Medusa listings endpoint and no dedicated public listings RPC. | Treat the helper as the implementation reference and migrate/replicate it into a Catalog API server service before demo delivery. Do not create a Medusa read endpoint merely to proxy public data. |
| Listing fields | The helper returns listing id, store id/name, unit price/currency, quantity, condition, language, finish, edition, and preorder flag. `listing_media` exists but is explicitly UI-deferred and is not read by the helper. | `seller_listings` plus public store data. | These fields cover the initial seller-row DTO. Listing photos are out of the first listings contract. |
| Default order | The helper orders only `unit_price ASC`. | Existing helper behavior. | This satisfies the current default lowest-price rule, but it is not a selectable sorting capability. |
| Selectable listing order / pagination | No public API, RPC, or Storefront helper accepts sort criteria, limit, or offset for a product's listings. | Missing capability. | Add them deliberately to the future Catalog listings service contract; do not make the UI sort an already truncated result set. |
| Chiki-Elección recommendation | `@chiki/search#getCatalogListingRecommendation(client, catalogItemId)` calls the public security-definer RPC `resolve_catalog_listing_recommendation(uuid)`. It returns one mode: `manual`, `automatic`, or `none`, plus the recommended eligible listing when one exists. | Public Supabase RPC wrapped by `@chiki/search`; it is safe for Storefront server use. | Use it as a separate, parallel source for the featured recommendation. It is not the listings feed and must not replace it. |
| Manual Chiki-Elección | `catalog_listing_recommendation_overrides` stores an HQ-selected listing. `apps/medusa/src/api/marketplace/admin/chiki-choice/[catalogItemId]/route.ts` is its protected management endpoint. | Medusa/admin writes; public RPC resolves the effective buyer-facing result. | Buyer UI never writes or reads overrides directly. A stale/hidden manual override automatically falls back to the automatic choice. |
| Automatic Chiki-Elección | The resolver chooses the lowest-price eligible listing, tie-breaking by listing id. It requires a public CCI, active listing, stock, non-preorder status, commerce-ready store, and respects `hide_non_chiki_listings`. | `resolve_catalog_listing_recommendation` RPC. | A recommendation can validly be `none` even when the product exists. It must be treated as a listing concern, not an absent product. |

### Important current mismatches

1. `getActiveListingsForCci` includes preorder listings, while the Chiki-Elección
   resolver deliberately excludes them. The new listings contract must state
   whether preorder rows belong in this rule or in the existing separate preorder
   presentation.
2. The helper applies the Chiki-only kill switch but does not itself filter
   `is_store_commerce_ready`; the recommendation resolver does. The Catalog API
   service should align feed eligibility with the authoritative resolver before
   it becomes the reusable source for product detail.
3. The current helper swallows database/settings failures into `[]`, which makes
   an outage indistinguishable from a genuine no-listings state. The new service
   contract needs an explicit error result.

### Recommended W2-T2 service boundary

Create a server-only Catalog service operation that reads the feed and the
recommendation independently, in parallel, and returns separate fields:

```ts
getCatalogProductListings(catalogItemId: string, config?: {
  order?: "price_asc" | "price_desc";
  limit?: number;
  offset?: number;
}): Promise<{
  listings: CatalogProductListing[];
  recommendation: CatalogListingRecommendation | null;
  pagination: { offset: number; nextOffset: number | null; hasMore: boolean };
  error: { code: string; message: string } | null;
}>
```

The exact row and UI models remain a W2-T2 / UI-contract decision. This shape
only preserves the authority split: canonical product read, listings feed, and
Chiki-Elección recommendation are distinct capabilities.

## Cross-layer model ownership

- **Medusa DTOs and persistence-facing inputs** belong to Medusa route and `_lib` code.
- **Storefront API contracts and mappings** belong in `apps/storefront/apis/<journey>/domain/contracts` and service adapters.
- **Screen-facing data types** belong in `@chiki/ui/marketplace-v2`; `apps/storefront/apis/domain.index.ts` may re-export only the front types deliberately shared with demo.
- A model change must be traced in this order: behavior invariant → Medusa DTO/route → API mapping and public contract → demo integration → UI prop contract. If the backend representation does not change, the first affected layer becomes the source of the change.

## Consultation protocol

The capability worker consults and updates this map before implementation begins. If
the requested operation, authority, model mapping, or reuse decision is absent or
contradictory, it researches the relevant repository surfaces and records the outcome
with evidence before dependent work continues.
