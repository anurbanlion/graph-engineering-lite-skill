# Use Cases - `home`

## Route: `/demo/` (Home Screen)

### 1. Service Scenarios (`apps/storefront/apis`)

```yaml
scenario:
  name: "Load Home showcase content (Hero Banners + Highlights + Trending + Best Sellers)"
  given: "The visitor navigates to the primary storefront page."
  when: "The Server Component executes the service call."
  then:
    - "The Hero Banners, Highlights, Trending, and Best Sellers content is retrieved."
    - "The result is delivered to the corresponding component."
  builder_suggestions:
    kind: "query"
    place: "Page Server Component"
    origin_journey: "home"
    service: "getStorefrontShowcase(): Promise<StorefrontShowcase | null>"
    service_status: "exposed"
    return_front_type: "StorefrontShowcase | null"
    return_front_type_status: "not exposed"
```

### 2. Interactive Scenarios

| Behaviour Boundary | Scenario | Implementation suggestion |
| :--- | :--- | :--- |
| **Redirection** | **Display not found screen on showcase (null)**<br/>**Given:** The visitor navigates to the storefront home route.<br/>**When:** The storefront showcase data resolves to null.<br/>**Then:** The application renders the not found error screen. | Server Component guard: call `notFound()` from `next/navigation` when `getStorefrontShowcase()` returns `null`. |

### 3. Declarative (NO-OP) Scenarios

| Behaviour Boundary | Scenario | Implementation suggestion |
| :--- | :--- | :--- |
| **Redirection** | **Display error screen on showcase failure**<br/>**Given:** The visitor navigates to the storefront home route.<br/>**When:** The storefront showcase service throws an unhandled exception.<br/>**Then:** The application renders the system error screen. | Automatic Next.js error boundary (`error.tsx`): no custom implementation required as unhandled Server Component exceptions trigger it automatically. |
| **Navigation** | **Promotional campaign card navigation**<br/>**Given:** A promotional campaign card is active in the home showcase.<br/>**When:** The visitor clicks the card or its call-to-action button.<br/>**Then:** The visitor is navigated to the target catalog view or promotion destination. | Link destination pattern: `href: /catalog?campaign=${campaignSlug}` or `/catalog/${itemSlug}`. |
| **Navigation** | **Product detail navigation from best sellers**<br/>**Given:** The best seller product grid is displayed.<br/>**When:** The visitor clicks a product card.<br/>**Then:** The visitor is navigated directly to the detail view of the selected product. | Link destination pattern: `href: /catalog/${productSlug}`. |
| **Navigation** | **Informational link navigation from footer**<br/>**Given:** The visitor scrolls to the footer section.<br/>**When:** The visitor clicks an informational or policy link.<br/>**Then:** The visitor is navigated to the corresponding static content page without a full application reload. | Static link destinations: `href: /terms`, `href: /returns`, `href: /privacy`. |


---

## Route: `/demo/layout` (Storefront Header)

### 1. Service Scenarios (`apps/storefront/apis`)

```yaml
scenario:
  name: "Retrieve authenticated user"
  given: "The universal layout prepares the navigation menu."
  when: "The component executes the service call."
  then:
    - "The verified identity of the user is retrieved."
    - "The result is delivered to the corresponding component."
  builder_suggestions:
    kind: "query"
    place: "Layout Server Component"
    origin_journey: "account"
    service: "getCurrentUser(): Promise<CurrentUser | null>"
    service_status: "exposed"
    return_front_type: "CurrentUser | null"
    return_front_type_status: "exposed"
```

```yaml
scenario:
  name: "Retrieve shopping cart summary"
  given: "The universal layout prepares the shopping cart button and badge."
  when: "The component executes the service call."
  then:
    - "The shopping cart summary (item count and navigation destination) is retrieved."
    - "The result is delivered to the corresponding component."
  builder_suggestions:
    kind: "query"
    place: "Layout Server Component"
    origin_journey: "cart"
    service: "getCartSummary(): Promise<CartSummary | null>"
    service_status: "exposed"
    return_front_type: "CartSummary | null"
    return_front_type_status: "not exposed"
```

```yaml
scenario:
  name: "Retrieve navigation menu information"
  given: "The universal layout prepares the navigation menu."
  when: "The component executes the service call."
  then:
    - "The navigation menu information is retrieved."
    - "The result is delivered to the corresponding component."
  builder_suggestions:
    kind: "query"
    place: "Layout Server Component"
    origin_journey: "home"
    service: "getStorefrontMenu(): Promise<StorefrontMenu | null>"
    service_status: "exposed"
    return_front_type: "StorefrontMenu | null"
    return_front_type_status: "not exposed"
```

```yaml
scenario:
  name: "Retrieve footer information"
  given: "The universal layout prepares the footer."
  when: "The component executes the service call."
  then:
    - "The footer information is retrieved."
    - "The result is delivered to the corresponding component."
  builder_suggestions:
    kind: "query"
    place: "Layout Server Component"
    origin_journey: "home"
    service: "getStorefrontFooter(): Promise<StorefrontFooter | null>"
    service_status: "exposed"
    return_front_type: "StorefrontFooter | null"
    return_front_type_status: "not exposed"
```

```yaml
scenario:
  name: "Request sign-out service"
  given: "The user intends to sign out."
  when: "The component needs to invoke the sign-out service."
  then:
    - "The sign-out service is invoked."
    - "Session cookies and credentials are purged."
    - "The page is revalidated."
    - "Confirmation or errors are delivered to the component."
  builder_suggestions:
    kind: "mutation"
    place: "Shell Client Component"
    origin_journey: "account"
    service: "logoutUser(): Promise<ActionResult>"
    service_status: "exposed"
    return_front_type: "ActionResult"
    return_front_type_status: "not exposed"
```

### 2. Interactive Scenarios

```yaml
scenario:
  name: "Sign out user"
  given:
    - "The user has an active authenticated session."
  when:
    - "The user clicks sign out in the navigation menu."
  then:
    - "The session is revoked in the identity provider."
    - "If the operation results in error, the user is redirected to the home route."
    - "If the operation succeeds and the current route is unprotected, the user remains on the current route."
    - "If the operation succeeds and the current route is protected, the user is redirected to the home route."
  builder_suggestions:
    place: "Layout Client Component"
    handler: "handleLogOut()"
    services:
      - "logoutUser()"
```

### 3. Declarative (NO-OP) Scenarios

| Behaviour Boundary | Scenario | Implementation suggestion |
| :--- | :--- | :--- |
| **Navigation** | **Login access from anonymous state**<br/>**Given:** An unauthenticated guest visitor has the navigation menu open.<br/>**When:** The visitor clicks the "Sign In / Register" option.<br/>**Then:** The visitor is navigated to the authentication screen preserving the current route to return after logging in. | Navigation link pattern: `href: /login?from=${encodeURIComponent(currentPath)}`. |
| **Navigation** | **Category and account navigation from menu**<br/>**Given:** The navigation menu is open.<br/>**When:** The visitor selects a game catalog category or an account section.<br/>**Then:** The visitor is navigated to the selected catalog filter or account destination. | Navigation links mapped to: `href: /catalog?game=${gameId}`, `href: /account`, or `href: /orders`. |
| **Navigation** | **Cart navigation from header badge**<br/>**Given:** The header displays the cart pill control with the item counter.<br/>**When:** The visitor clicks the cart button.<br/>**Then:** The visitor is navigated to the cart summary screen. | Action link pattern: `href: /demo/cart`. |

---

## Design Notes

- **Separation of Contracts**: UI Data Models are omitted from this specification; data contracts belong exclusively to `design-journey-data-model`.
- **Architectural Scope**: The Universal Storefront Layout (`/demo/layout`) provides the shared navigation shell, user authentication resolution, cart badge synchronization, and slide-out navigation menu. The Home route (`/demo/`) composes page-specific content: hero banner carousel, hot promotional campaigns, and high-velocity best seller listings.
