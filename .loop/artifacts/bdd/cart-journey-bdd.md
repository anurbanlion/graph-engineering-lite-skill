# Use Cases - `cart`

> Location: `.graph-engineering/runs/cart-journey/design-journey-use-cases-spec/OUTPUT-20260907-2125.md`  
> Domain: `cart-journey`  
> Parent Layout: `apps/storefront/src/app/demo/(commerce)/layout.tsx`  
> Reconciled via: `design-journey-use-cases-spec`

---

## Route: `/demo/(commerce)/layout` (Transactional Commerce Layout)

### 1. Service Scenarios (`apps/storefront/apis`)

```yaml
scenario:
  name: "Retrieve authenticated user"
  given:
    - "The commerce layout prepares the shared transactional journey state."
  when: "The component executes the service call."
  then:
    - "The authenticated user is retrieved."
    - "The result is delivered to the corresponding provider."
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
  name: "Retrieve latest owned cart"
  given:
    - "The commerce layout prepares the shared transactional journey state."
    - "There is an authenticated user."
  when: "The component executes the service call."
  then:
    - "The active cart is reconciled against current inventory and prices."
    - "The latest active cart is delivered to the corresponding provider."
    - "If reconciliation changed the cart, the resulting cart change notice is delivered to the corresponding provider."
  builder_suggestions:
    kind: "query"
    place: "Layout Server Component"
    origin_journey: "cart"
    service: "getLatestOwnedCart(): Promise<CartSnapshot | null>"
    service_status: "exposed"
    return_front_type: "CartSnapshot | null"
    return_front_type_status: "exposed"
```

```yaml
scenario:
  name: "Retrieve buyer fiscal identities"
  given:
    - "An authenticated buyer profile is available."
  when: "The component executes the service call."
  then:
    - "The buyer fiscal identities are retrieved."
    - "The result is delivered to the corresponding provider."
  builder_suggestions:
    kind: "query"
    place: "Layout Server Component"
    origin_journey: "account"
    service: "getUserFiscalIdentities(userId)"
    service_status: "not exposed"
    return_front_type: "FiscalIdentityBook"
    return_front_type_status: "not exposed"
```

```yaml
scenario:
  name: "Retrieve buyer delivery addresses"
  given:
    - "An authenticated buyer profile is available."
  when: "The component executes the service call."
  then:
    - "The buyer delivery addresses are retrieved."
    - "The result is delivered to the corresponding provider."

  builder_suggestions:
    kind: "query"
    place: "Layout Server Component"
    origin_journey: "account"
    service: "getUserDeliveryAddresses(userId)"
    service_status: "not exposed"
    return_front_type: "DeliveryAddressBook"
    return_front_type_status: "not exposed"
```


### 2. Interactive Scenarios

| Behaviour Boundary | Scenario | Implementation suggestion |
| :--- | :--- | :--- |
| **Redirection** | **Handle no authenticated user**<br/>**Given:** An unauthenticated visitor enters the transactional commerce route group.<br/>**When:** Access is evaluated at the commerce route boundary.<br/>**Then:** The visitor is redirected to the authentication screen preserving the return path. | Route guard / middleware: Layout Server Component redirects unauthenticated requests to `/login?from=${encodeURIComponent(currentPath)}`. |

### 3. Declarative (NO-OP) Scenarios


| Behaviour Boundary | Scenario | Implementation suggestion |
| :--- | :--- | :--- |
| **Error Boundary** | **Handle unhandled commerce bootstrap failure**<br/>**Given:** The commerce layout retrieves the latest owned cart, buyer fiscal identities, and buyer delivery addresses.<br/>**When:** Any of those retrievals fails with an unhandled error.<br/>**Then:** The application renders the general demo error screen. | General demo route error boundary: `apps/storefront/src/app/demo/error.tsx`. |

---

## Route: `/demo/cart` (Active Cart Screen)

### 1. Service Operations (`apps/storefront/apis`)


```yaml
scenario:
  name: "Retrieve fulfillment options for cart store"
  given:
    - "The active cart contains a store group."
  when: "The component executes the service call."
  then:
    - "The available fulfillment options for the cart store are retrieved."
    - "The result is delivered to the corresponding component."
  builder_suggestions:
    kind: "query"
    place: "Page Server Component"
    origin_journey: "cart"
    service: "getFulfillmentOptions(storeIds: string[]): Promise<FulfillmentOptions[] | null>"
    service_status: "not exposed"
    return_front_type: "FulfillmentOptions[] | null"
    return_front_type_status: "not exposed"
    details:
      - "getFulfillmentOptions should accept an id array since we probably want to query several stores per call."
      - "FulfillmentOptions domain model is defined in contracts/cart.contract.ts but not yet re-exported in apis/domain.index.ts."
```

```yaml
scenario:
  name: "Request cart line quantity update service"
  given:
    - "The buyer intends to update the quantity of a cart line item."
  when: "The component needs to invoke the cart line quantity update service."
  then:
    - "The cart line quantity update service is invoked."
    - "The updated cart is returned."
    - "The shopping cart page cache is revalidated."
    - "Confirmation or errors are delivered to the corresponding component."
  builder_suggestions:
    kind: "mutation"
    place: "Shell Client Component"
    origin_journey: "cart"
    service: "updateCartLineQuantity(lineId: string, quantity: number): Promise<CartSnapshot>"
    service_status: "not exposed"
    return_front_type: "CartSnapshot"
    return_front_type_status: "exposed"
    details:
      - "Currently updateCartLineQuantity is exposed as a service and updateCartLineQuantityAction as an action, updateCartLineQuantityAction must be renamed to updateCartLineQuantity and the updateCartLineQuantity must be removed from use cases and public api index"
```

```yaml
scenario:
  name: "Request cart line removal service"
  given:
    - "The buyer intends to remove an item from the active cart."
  when: "The component needs to invoke the cart line removal service."
  then:
    - "The cart line removal service is invoked."
    - "The updated cart is returned."
    - "The shopping cart page cache is revalidated."
    - "Confirmation or errors are delivered to the corresponding component."
  builder_suggestions:
    kind: "mutation"
    place: "Shell Client Component"
    origin_journey: "cart"
    service: "removeCartLine(lineId: string): Promise<CartSnapshot>"
    service_status: "not exposed"
    return_front_type: "CartSnapshot"
    return_front_type_status: "exposed"
    details:
      - "Currently removeCartLine is exposed as a use case and removeCartLineAction as an action; removeCartLineAction must be renamed to removeCartLine and the use case must be removed from use cases and public api index."
```

```yaml
scenario:
  name: "Request save-for-later service"
  given:
    - "The buyer intends to move an active cart item to save-for-later."
  when: "The component needs to invoke the save-for-later service."
  then:
    - "The save-for-later service is invoked."
    - "The updated cart is returned."
    - "The shopping cart and saved items page caches are revalidated."
    - "Confirmation or errors are delivered to the corresponding component."
  builder_suggestions:
    kind: "mutation"
    place: "Shell Client Component"
    origin_journey: "cart"
    service: "moveCartLineToSavedItems(lineId: string): Promise<CartSnapshot>"
    service_status: "not exposed"
    return_front_type: "CartSnapshot"
    return_front_type_status: "exposed"
    details:
      - "Currently moveCartLineToSavedItems is exposed as a use case and moveCartLineToSavedItemsAction as an action; moveCartLineToSavedItemsAction must be renamed to moveCartLineToSavedItems and the use case must be removed from use cases and public api index."
```


### 2. Interactive Scenarios

```yaml
scenario:
  name: "Update cart line quantity"
  given:
    - "The buyer views the active cart containing items."
  when:
    - "The buyer changes the quantity of a line item via the quantity selector or dialog."
  then:
    - "While the operation is pending, cart interactions are locked."
    - "If the operation results in error, an error message is displayed to the buyer."
    - "If the operation succeeds, the cart subtotal and items are updated."
  builder_suggestions:
    place: "Shell Client Component"
    handler: "handleQuantityChange(lineId, quantity)"
    services:
      - "updateCartLineQuantityAction(lineId, quantity)"
```

```yaml
scenario:
  name: "Remove cart line item"
  given:
    - "The buyer views the active cart containing items."
  when:
    - "The buyer clicks the remove button on a cart line item."
  then:
    - "While the operation is pending, cart interactions are locked."
    - "If the operation results in error, an error alert is displayed to the buyer."
    - "If the operation succeeds, the cart subtotal is recalculated and the item disappears."
  builder_suggestions:
    place: "Shell Client Component"
    handler: "handleRemoveItem(lineId)"
    services:
      - "removeCartLineAction(lineId)"
```

```yaml
scenario:
  name: "Move cart line to saved items"
  given:
    - "The buyer views an item in the active cart."
  when:
    - "The buyer clicks 'Guardar para después' on a cart item."
  then:
    - "While the operation is pending, cart interactions are locked."
    - "If the operation results in error, a notification informs the buyer of the failure."
    - "If the operation succeeds, the line disappears from the active cart."
  builder_suggestions:
    place: "Shell Client Component"
    handler: "handleMoveToSaved(lineId)"
    services:
      - "moveCartLineToSavedItemsAction(lineId)"
```
| Behaviour Boundary | Scenario | Implementation suggestion |
| :--- | :--- | :--- |
| **Forward** | **Forward latest owned cart**<br/>**Given:** An authenticated buyer profile is available.<br/>**When:** The component executes the service call.<br/>**Then:** The latest active cart is retrieved.<br/>**And:** The result is delivered to the corresponding component. | Must read `cart` from `useCommerce()` and pass it to `Screen` component. |
| **Navigation** | **Return to previous page from cart subheader**<br/>**Given:** The buyer views the active cart screen.<br/>**When:** The buyer clicks the X control in the subheader.<br/>**Then:** The buyer returns to the previous page. | Shell Client Component handler: `handleReturnToPreviousPage()` invokes `router.back()`. |
| **Local State** | **Display cart mutation failure notice**<br/>**Given:** A cart mutation cannot be completed.<br/>**When:** The operation returns an error.<br/>**Then:** The cart notice is updated to tell the buyer to try again. | CommerceProvider state: `setNotice({ severity: "warning", message: "Intenta nuevamente" })`. |
| **Local State** | **Update shared fulfillment selection**<br/>**Given:** A store group displays its available fulfillment methods.<br/>**When:** The buyer selects delivery or pickup for that store.<br/>**Then:** The shared fulfillment selection state is updated for the store without mutating the cart lines.<br/>**And:** The estimated visual total is recalculated for the selected fulfillment option. | CommerceProvider exposes fulfillmentSelections and setFulfillmentSelection(selection); CartScreen derives the estimated total from the selection and fulfillment options. |




### 3. Declarative (NO-OP) Scenarios

| Behaviour Boundary | Scenario | Implementation suggestion |
| :--- | :--- | :--- |
| **Local UI Fallback** | **Fallback to pickup when fulfillment options are unavailable**<br/>**Given:** A cart store requires its fulfillment options.<br/>**When:** Retrieving fulfillment options for the cart store fails.<br/>**Then:** The fulfillment option pill is not displayed and the store is treated as pickup. | CartShell keeps fulfillment options unavailable; CartScreen hides the fulfillment pill and uses pickup as the local fallback. |
| **Navigation** | **Product detail navigation from cart item**<br/>**Given:** An item is listed in the active cart.<br/>**When:** The buyer clicks the product card image or title.<br/>**Then:** The buyer is navigated directly to the single product detail view. | Link destination pattern: `href: /demo/catalog/${itemSlug}`. |
| **Navigation** | **Store profile navigation from merchant group**<br/>**Given:** A store group header displays the merchant name and emblem.<br/>**When:** The buyer clicks the store name link.<br/>**Then:** The buyer is navigated to the store profile and merchant showcase. | Link destination pattern: `href: /demo/store/${storeSlug}`. |
| **Navigation** | **Switch view to saved items**<br/>**Given:** The buyer is on the active cart screen.<br/>**When:** The buyer clicks the "Guardados" tab in the cart header.<br/>**Then:** The application navigates to the saved items view. | Link destination pattern: `href: /demo/cart/saved`. |
| **Navigation** | **Proceed to checkout funnel**<br/>**Given:** The active cart contains purchasable items and no blocking validation errors.<br/>**When:** The buyer clicks the "Ir a pagar" primary action button.<br/>**Then:** The buyer is navigated to Step 1 of the checkout funnel. | Link destination pattern: `href: /demo/checkout`. |

---

## Route: `/demo/cart/saved` (Saved Items Screen - Guardados)

### 1. Service Operations (`apps/storefront/apis`)

```yaml
scenario:
  name: "Retrieve latest saved items"
  given:
    - "An authenticated buyer accesses the saved items route."
  when: "The component executes the service call."
  then:
    - "Saved listings are reconciled against current availability and prices."
    - "The latest saved items snapshot is returned."
    - "The result is delivered to the corresponding component."
    - "If reconciliation changed saved items, the resulting notice is delivered to the corresponding component."
  builder_suggestions:
    kind: "query"
    place: "Page Server Component"
    origin_journey: "cart"
    service: "getLatestSavedItems(): Promise<SavedItemsSnapshot>"
    service_status: "exposed"
    return_front_type: "SavedItemsSnapshot"
    return_front_type_status: "not exposed"
    details:
      - "Currently SavedItemsSnapshot is defined in cart/domain/contracts/cart.contract.ts (aliased to LatestSavedItems) but is not exported in apps/storefront/apis/domain.index.ts; it must be exposed in domain.index.ts as the canonical domain entity for the saved items route."
```

```yaml
scenario:
  name: "Request saved item to active cart service"
  given:
    - "The buyer intends to move an in-stock saved item to the active cart."
  when: "The component needs to invoke the saved item to active cart service."
  then:
    - "The saved item to active cart service is invoked."
    - "The updated cart snapshot is returned."
    - "The shopping cart and saved items page caches are revalidated."
    - "Confirmation or errors are delivered to the corresponding component."
  builder_suggestions:
    kind: "mutation"
    place: "Shell Client Component"
    origin_journey: "cart"
    service: "moveSavedItemToCart(listingId: string): Promise<CartSnapshot>"
    service_status: "not exposed"
    return_front_type: "SavedItemsSnapshot"
    return_front_type_status: "not exposed"
    details:
      - "Preserves original BDD scenario name ('Request saved item to active cart service')."
      - "Currently moveSavedItemToCart is exposed as a use case and moveSavedItemToCartAction as an action; moveSavedItemToCartAction must be renamed to moveSavedItemToCart and the use case removed from public index."
      - "Return type is standardized to CartSnapshot (exposed in domain.index.ts) to provide the updated reconciled cart state to the client shell."
```

```yaml

scenario:
  name: "Request saved item removal service"
  given:
    - "The buyer intends to remove an item from the saved list."
  when: "The component needs to invoke the saved item removal service."
  then:
    - "The saved item removal service is invoked."
    - "The operation outcome is returned."
    - "The saved items page cache is revalidated."
    - "Confirmation or errors are delivered to the corresponding component."
  builder_suggestions:
    kind: "mutation"
    place: "Shell Client Component"
    origin_journey: "cart"
    service: "removeSavedItem(listingId: string): Promise<void>"
    service_status: "not exposed"
    return_front_type: "SavedItemsSnapshot"
    return_front_type_status: "not exposed"
    details:
      - "Currently removeSavedItem is exposed as a use case and removeSavedItemAction as an action; removeSavedItemAction must be renamed to removeSavedItem and the use case removed from public index."
      - "The return type void represents a stateful dismissal without payload; void is treated as an exposed language primitive."
```

### 2. Interactive Scenarios

```yaml
scenario:
  name: "Restore saved item to cart"
  given:
    - "The buyer views the saved items list."
    - "A saved card listing is available for purchase."
  when:
    - "The buyer clicks 'Mover al carrito' on the saved item."
  then:
    - "While the operation is pending, saved item interactions are locked."
    - "If the operation results in error, an error message is displayed to the buyer."
    - "If the operation succeeds, the item is removed from the saved list."
  builder_suggestions:
    place: "Shell Client Component"
    handler: "handleMoveToCart(listingId)"
    services:
      - "moveSavedItemToCartAction(listingId)"
```

```yaml
scenario:
  name: "Remove saved item"
  given:
    - "The buyer views an item in the saved items list."
  when:
    - "The buyer clicks 'Eliminar' on the saved item."
  then:
    - "While the operation is pending, saved item interactions are locked."
    - "If the operation results in error, an error message is displayed to the buyer."
    - "If the operation succeeds, the item is removed from the saved list."
  builder_suggestions:
    place: "Shell Client Component"
    handler: "handleRemoveSavedItem(listingId)"
    services:
      - "removeSavedItemAction(listingId)"
```

| Behaviour Boundary | Scenario | Implementation suggestion |
| :--- | :--- | :--- |
| **Navigation** | **Return to previous page from saved items subheader**<br/>**Given:** The buyer views the saved items screen.<br/>**When:** The buyer clicks the X control in the subheader.<br/>**Then:** The buyer returns to the previous page. | Shell Client Component handler: `handleReturnToPreviousPage()` invokes `router.back()`. |

### 3. Declarative (NO-OP) Scenarios

| Behaviour Boundary | Scenario | Implementation suggestion |
| :--- | :--- | :--- |
| **Redirection** | **Display error screen when loading saved items fails**<br/>**Given:** The buyer navigates to /demo/cart/saved.<br/>**When:** Retrieving latest saved items fails with an unhandled error.<br/>**Then:** The application redirects to the general demo error screen with retry options. | General demo error route: apps/storefront/src/app/demo/error.tsx. |
| **Navigation** | **Switch view to active cart**<br/>**Given:** The buyer is on the saved items screen.<br/>**When:** The buyer clicks the "Carrito" tab in the header.<br/>**Then:** The application navigates to the active shopping cart view. | Link destination pattern: `href: /demo/cart`. |
| **Navigation** | **Product detail navigation from saved item**<br/>**Given:** An item is listed in the saved items list.<br/>**When:** The buyer clicks the saved card title or artwork.<br/>**Then:** The buyer is navigated directly to the single product detail view. | Link destination pattern: `href: /demo/catalog/${itemSlug}`. |

---

## Design Notes

- **Shared Transactional Layout Context (apps/storefront/src/app/demo/(commerce)/layout.tsx)**:
  - The cart journey and checkout journey share the (commerce) transactional route group layout. This isolates transactional flows (/demo/cart, /demo/cart/saved, /demo/checkout, /demo/checkout/delivery, /demo/checkout/payment) from marketing distractions.
  - The Layout Server Component retrieves the active cart, authenticated buyer, fiscal identities, and delivery addresses, then delivers each result to CommerceProvider.
  - CommerceProvider initializes fulfillmentSelections as null; CartShell resolves and updates selections only after the buyer chooses fulfillment for a store.
- **Page Server Component Boundary (cart/page.tsx, cart/saved/page.tsx)**:
  - Cart reads the active cart from CommerceProvider; saved items remain a route-specific retrieval through getLatestSavedItems(), which reconciles availability and prices before delivery.
- **Shell Client Component Boundary (cart/shell.tsx, cart/saved/shell.tsx)**:
  - CartShell passes cart, fulfillmentSelections, and route-specific fulfillment options to CartScreen, and updates the shared cart after cart mutations.
  - Client components manage transition boundaries and user mutation handlers.

- **Latest Transactional Retrieval**:
  - Latest cart and saved-item retrieval reconcile marketplace changes during the initial route load and deliver a notice when reconciliation changed the persisted state.
- **Separation of Contracts**:
  - UI Data Models and DTO schema definitions are omitted from this specification; data contracts belong exclusively to `design-journey-data-model`.
