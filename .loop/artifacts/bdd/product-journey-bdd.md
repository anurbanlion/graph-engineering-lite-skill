# Use Cases - `product`

## Route: `/catalog/[slug]` (Product Detail Page)

### 1. Service Operations (`apps/storefront/apis`)

```yaml
scenario:
  name: "Load canonical product detail"
  given: "A visitor or buyer navigates to the product detail page."
  when: "The Server Component executes the product retrieval service."
  then:
    - "The canonical product aggregate is resolved with relations, card details, active seller offers, and authoritative Chiki-Choice recommendation."
    - "The result is delivered to the corresponding component."
  builder_suggestions:
    place: "Page Server Component"
    service: "getProduct(slug, lang)"
    return_front_type: "ProductCardDetail | null"
```

```yaml
scenario:
  name: "Select requested active listing by query parameter"
  given:
    - "A product has been retrieved with active marketplace listings."
    - "The request URL contains a listing selection query parameter."
  when: "The Server Component executes the listing selection helper before rendering."
  then:
    - "The requested seller listing is evaluated for availability and active stock."
    - "If valid, the requested offer is selected; otherwise, the default Chiki-Choice offer is retained."
    - "The result is delivered to the corresponding component."
  builder_suggestions:
    place: "Page Server Component"
    service: "selectRequestedActiveListing(listings, listingId)"
    return_front_type: "ProductListing | null"
```

```yaml
scenario:
  name: "Request add seller offer to cart service"
  given: "The buyer intends to add a selected seller offer and quantity to the cart."
  when: "The component invokes the add-to-cart service action."
  then:
    - "The listing item addition is submitted to the marketplace cart service."
    - "The cart route cache is revalidated."
    - "The mutation status and updated cart count are returned to the caller."
  builder_suggestions:
    place: "Shell Client Component"
    service: "addProductToCart(listingId, quantity, from)"
    return_front_type: "AddProductToCartResult"
```

```yaml
scenario:
  name: "Request immediate checkout service"
  given: "The buyer intends to purchase a selected seller offer immediately."
  when: "The component invokes the direct purchase service action."
  then:
    - "The listing is added to the active cart."
    - "The user session is transferred to the checkout funnel."
    - "Any authentication challenge or failure result is delivered to the caller."
  builder_suggestions:
    place: "Shell Client Component"
    service: "buyProductNow(listingId, quantity, from)"
    return_front_type: "AddProductToCartResult"
```

### 2. Interactive Scenarios

```yaml
scenario:
  name: "Add product listing to cart"
  given:
    - "The buyer views an available product with an active seller offer."
  when:
    - "The buyer selects a quantity and clicks 'Añadir al carrito'."
  then:
    - "The selected listing and quantity are added to the active shopping cart."
    - "If the user is unauthenticated, the user is redirected to the login route preserving the return URL."
    - "If the operation succeeds, the cart feedback drawer is displayed with item details and the header cart badge refreshes."
    - "If the operation results in error, an error message is presented without navigating away."
  builder_suggestions:
    place: "Shell Client Component"
    handler: "handleAddToCart()"
    services:
      - "addProductToCart(listingId, quantity, from)"
```

```yaml
scenario:
  name: "Buy product listing immediately"
  given:
    - "The buyer views an available product with an active seller offer."
  when:
    - "The buyer clicks 'Comprar ahora'."
  then:
    - "The selected listing and quantity are added to the cart and the buyer is transferred to checkout."
    - "If the user is unauthenticated, the user is redirected to the login route preserving the return URL."
    - "If the operation succeeds, the browser navigates directly to the checkout route."
    - "If the operation results in error, an error message is presented and the user remains on the product page."
  builder_suggestions:
    place: "Shell Client Component"
    handler: "handleBuyNow()"
    services:
      - "buyProductNow(listingId, quantity, from)"
```

| Behaviour Boundary | Scenario | Implementation suggestion |
| :--- | :--- | :--- |
| **Redirection** | **Display not found screen on missing or inactive product**<br/>**Given:** A visitor requests a product URL with a slug that does not exist or is inactive in the catalog.<br/>**When:** The Server Component evaluates the product retrieval service response.<br/>**Then:** The application invokes `notFound()` and renders the standardized 404 error screen. | Server Component guard: call `notFound()` from `next/navigation` when `getProduct(slug, lang)` returns `null`. |
| **Redirection** | **Display error screen on product load failure**<br/>**Given:** A visitor navigates to the product detail route.<br/>**When:** The product data service throws an unhandled exception.<br/>**Then:** The application captures the failure and renders the system error screen. | Automatic Next.js error boundary (`error.tsx`): no custom implementation required as unhandled Server Component exceptions trigger it automatically. |
| **Redirection** | **Guest purchase redirect to authentication**<br/>**Given:** An unauthenticated visitor interacts with purchasing actions ("Añadir al carrito" or "Comprar ahora").<br/>**When:** The Server Action returns an `auth_required` status.<br/>**Then:** The application redirects the user to `/login?from=/catalog/[slug]` preserving the current route for post-login return. | Server Action guard returning `loginHref: /login?from=${encodeURIComponent(currentPath)}` followed by client navigation via `router.push(loginHref)`. |
| **Local State** | **Promote selected seller listing to active Buy Box**<br/>**Given:** The product detail page displays multiple seller offers in the listings table.<br/>**When:** The user selects an alternative seller listing row.<br/>**Then:** The selected listing is promoted to the active Buy Box, updating price, shipping fee, seller badges, and available stock. | Shell state: `selectedOfferId` state hook (`setSelectedOfferId`) in `ProductDetailShell`. |
| **Local State** | **Adjust purchase quantity for active offer**<br/>**Given:** An active listing is selected in the Buy Box with available quantity greater than one.<br/>**When:** The user changes the quantity selector control.<br/>**Then:** The active purchase quantity state updates within the allowable stock limit. | Shell state: `quantity` state hook (`setQuantity`) in `ProductDetailShell`. |
| **Local State** | **Sort seller listings dynamically**<br/>**Given:** The seller listings table presents multiple marketplace offers.<br/>**When:** The user toggles or selects a sort option (e.g., "Barato a Caro" vs "Mejor Condición").<br/>**Then:** The visible listings reorder in memory according to the selected criterion without issuing a network request. | Shell state: `sortLabel` state hook (`setSortLabel`) in `ProductDetailShell`. |
| **Local State** | **Cart feedback drawer visibility and dismiss**<br/>**Given:** A seller offer has been added to the cart.<br/>**When:** The mutation succeeds or the user dismisses the notice.<br/>**Then:** The bottom feedback drawer displays the added product details and controls its visibility state. | Shell state: `feedbackNotice` state hook (`setFeedbackNotice`) in `ProductDetailShell`. |
| **Local State** | **Smooth scroll to seller listings section**<br/>**Given:** The Buy Box displays the link to view alternative seller offers.<br/>**When:** The user clicks "Ver otros listados".<br/>**Then:** The window scrolls smoothly to the listings container without altering the route or history state. | Shell client event: `element.scrollIntoView({ behavior: 'smooth' })` targeting `[data-testid="listings-section"]`. |

### 3. Declarative (NO-OP) Scenarios

| Behaviour Boundary | Scenario | Implementation suggestion |
| :--- | :--- | :--- |
| **Navigation** | **Breadcrumb navigation to catalog or game**<br/>**Given:** The product detail page renders the breadcrumb trail.<br/>**When:** The visitor clicks the catalog or game segment in the breadcrumb trail.<br/>**Then:** The visitor navigates to the game-filtered catalog view. | Breadcrumb link pattern: `href: /demo/catalog?game=${gameSlug}` or `/demo/catalog`. Purpose: Ascend navigation hierarchy. |
| **Navigation** | **Catalog expansion set navigation**<br/>**Given:** The product is associated with an expansion set.<br/>**When:** The visitor clicks the expansion set name link or "Ver expansión" button.<br/>**Then:** The visitor navigates to the catalog filtered by that expansion set. | Link destination pattern: `href: /demo/catalog?expansion=${expansionSlug}`. Purpose: Explore other cards from the same set. |
| **Navigation** | **Alternative print editions search navigation**<br/>**Given:** The product possesses alternative printings or art variants.<br/>**When:** The visitor clicks the "Otros prints" action link.<br/>**Then:** The visitor navigates to the catalog search results matching the card title. | Link destination pattern: `href: /demo/catalog?q=${encodeURIComponent(productTitle)}`. Purpose: Discover alternative printings and artwork variants. |
| **Navigation** | **Merchant store profile navigation**<br/>**Given:** A seller listing displays the merchant store identity and verified badges.<br/>**When:** The visitor clicks the merchant name or store link.<br/>**Then:** The visitor navigates to the merchant's dedicated public storefront. | Link destination pattern: `href: /demo/store/${sellerSlug}`. Purpose: Inspect merchant inventory and seller credentials. |
| **Navigation** | **Cart review navigation from feedback notice**<br/>**Given:** The add-to-cart confirmation notice is displayed.<br/>**When:** The visitor clicks the "Ver carrito" call-to-action button.<br/>**Then:** The visitor navigates directly to the shopping cart screen. | Action link pattern: `href: /demo/cart`. Purpose: View cart contents and proceed to checkout. |
| **Navigation** | **Preorder terms and guarantees link navigation**<br/>**Given:** The product detail page renders an active preorder reservation panel.<br/>**When:** The visitor clicks the preorder policy or guarantee details link.<br/>**Then:** The visitor navigates to the informational terms and policies page without application reload. | Static link destination pattern: `href: /terms#preorders` or `/help/preorders`. Purpose: Review preorder terms and fulfillment timelines. |

## Design notes

- **Separation of Contracts**: UI Data Models are omitted from this specification; data contracts belong exclusively to `design-journey-data-model`.
- **Architectural Scope**: The Product Detail Page (`/demo/catalog/[slug]`) operates within the Universal Storefront Layout (`/demo/layout`). Page-level server component handles data fetching (`getProduct`) and query-based listing selection (`selectRequestedActiveListing`). Interactive state (quantity selection, active listing selection, in-memory sorting, feedback drawer, and cart mutations) is encapsulated in `ProductDetailShell`.
- **Declarative vs Interactive Segregation**: All link-driven navigations (expansion set filters, alternative print searches, store profiles, breadcrumbs, and cart redirection from the notice) are classified as declarative NO-OP scenarios to prevent redundant implementation tasks while maintaining full UX traceability.
- **Authentication Handshake**: Purchasing actions require an authenticated user. Unauthenticated attempts result in an `auth_required` response from server actions, routing the buyer to `/login?from=/catalog/[slug]` before resuming the purchase flow.

## Focused refinement questions

- None. The contract signatures, aggregate types, and shell interaction boundaries are fully reconciled with existing contracts in `apps/storefront/apis/product/` and presentational components in `@chiki/ui/marketplace-v2`.
