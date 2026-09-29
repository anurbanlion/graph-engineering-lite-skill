# Use Cases - `checkout`

## Route: `/demo/(commerce)/layout` (Transactional Commerce Layout)

> **Gobernanza centralizada en Cart Journey**:  
> El layout transaccional común `/demo/(commerce)/layout`, su guardia de autenticación (`redirect('/login?from=' + encodeURIComponent(returnPath))`), y el bootstrap de datos compartidos (`user: AccountProfile`, `fiscalIdentities: BuyerFiscalIdentitiesBook`, `deliveryAddresses: CustomerAddress[]`, `cart: CartSnapshot`, y `fulfillmentSelections`) ya están completamente controlados e implementados por el **Cart Journey** a través de `CommerceLayout` y `CommerceProvider` (`apps/storefront/src/app/demo/(commerce)/layout.tsx`).  
> 
> Por lo tanto, no es necesario duplicar escenarios ni servicios de bootstrap en el journey de checkout. Las rutas y shells de checkout consumen directamente el estado compartido mediante `useCommerce()`.

---

## Route: `/demo/checkout` (Personal and Fiscal Data)

### 1. Service Operations (`apps/storefront/apis`)

```yaml
scenario:
  name: "Request save buyer fiscal identity service"
  given:
    - "The buyer intends to save or update electronic billing fiscal identity details."
  when: "The component needs to invoke the save buyer fiscal identity service."
  then:
    - "The save buyer fiscal identity service is invoked."
    - "The new fiscal identity is designated as default in the buyer fiscal identities book."
    - "The updated fiscal identity book is returned."
    - "Confirmation or errors are delivered to the corresponding component."
  builder_suggestions:
    kind: "mutation"
    place: "Shell Client Component"
    origin_journey: "account"
    service: "saveFiscalIdentity(newFiscalIdentity): Promise<FiscalIdentityBook>"
    service_status: "not exposed"
    return_front_type: "FiscalIdentityBook"
    return_front_type_status: "exposed"
```

### 2. Interactive Scenarios

```yaml
scenario:
  name: "Save buyer fiscal identity"
  given:
    - "The buyer is on the personal information step."
    - "The buyer checks 'Solicitar factura' and enters a valid RUC and business name."
  when:
    - "The buyer saves or confirms the fiscal identity."
  then:
    - "The fiscal identity is persisted in the buyer account."
    - "If the operation results in error, an error toast notification is displayed."
    - "If the operation succeeds, the fiscal identity is selected for invoicing."
  builder_suggestions:
    place: "Shell Client Component"
    handler: "handleSaveFiscalIdentity(newFiscalIdentity)"
    services:
      - "saveFiscalIdentity(newFiscalIdentity)"
    details:
      - The updated FiscalIdentityBook must be saved on the CommerceProvider
```

| Behaviour Boundary | Scenario | Implementation suggestion |
| :--- | :--- | :--- |
| **Redirection** | **Handle empty cart**<br/>**Given:** An authenticated buyer accesses `/demo/checkout`.<br/>**When:** The active cart contains zero items or is null.<br/>**Then:** The application redirects the buyer back to `/demo/cart`. | Shell guard: If `!cart \|\| cart.storeGroups.length === 0`, `router.replace('/demo/cart')`. |
| **Forward** | **Forward buyer fiscal identities**<br/>**Given:** An authenticated buyer profile is available.<br/>**When:** The component executes the service call.<br/>**Then:** The buyer fiscal identities are retrieved.<br/>**And:** The result is delivered to the corresponding component. | Must read `fiscalIdentities` from `useCommerce()` and pass it to `Screen` component. |
| **Forward** | **Forward buyer fulfillment selections**<br/>**Given:** Active store fulfillment selections are available in commerce context.<br/>**When:** The component executes the service call.<br/>**Then:** The buyer fulfillment selections are retrieved.<br/>**And:** The result is delivered to the corresponding component. | Must read `fulfillmentSelections` from `useCommerce()` and pass it to `Screen` component. |
| **Local State** | **Toggle invoice request**<br/>**Given:** The buyer views personal data inputs (Nombre, N° Documento, Teléfono).<br/>**When:** The buyer toggles the 'Solicitar factura' checkbox.<br/>**Then:** When checked, reveals the 'N° RUC' (and business name/saved identities) input fields.<br/>**And:** When unchecked, defaults to standard Boleta using personal document credentials. | Shell state: `handleToggle(isRequested)` using local `setState` with `isInvoiceRequested`. |
| **Local State** | **Modify fiscal identity form data**<br/>**Given:** The buyer views the fiscal identity form.<br/>**When:** The buyer edits any fiscal identity field.<br/>**Then:** The shell updates the fiscal identity form data in local state until saved. | Shell state: `handleFiscalIdentityFormChange(fields)` using local `setState` to store and manage form information, potentially using `react-hook-form`. |
| **Navigation** | **Return to cart from checkout header**<br/>**Given:** The buyer is on the personal data step.<br/>**When:** The buyer clicks the back arrow or close button.<br/>**Then:** The buyer is navigated back to `/demo/cart`. | Shell handler: `router.back()` or link to `/demo/cart`. |

### 3. Declarative (NO-OP) Scenarios

| Behaviour Boundary | Scenario | Implementation suggestion |
| :--- | :--- | :--- |
| **Navigation** | **Step progression to delivery**<br/>**Given:** Personal and fiscal data are valid and at least one store group requires home delivery.<br/>**When:** The buyer clicks "Continuar".<br/>**Then:** The shell navigates to the shipping address step. | Client navigation: `router.push('/demo/checkout/delivery')`. |
| **Navigation** | **Step progression bypassing delivery for pickup-only**<br/>**Given:** Personal and fiscal data are valid and all store groups are configured as store pickup.<br/>**When:** The buyer clicks "Continuar".<br/>**Then:** The shell bypasses shipping and navigates directly to payment. | Client navigation: `router.push('/demo/checkout/payment')`. |

---

## Route: `/demo/checkout/delivery` (Shipping and Fulfillment)

### 1. Service Operations (`apps/storefront/apis`)

```yaml
scenario:
  name: "Retrieve checkout shipping and fulfillment data"
  given:
    - "An authenticated buyer accesses the delivery step (/demo/checkout/delivery)."
  when: "The component executes the service call."
  then:
    - "Saved delivery addresses and seller fulfillment options are retrieved."
    - "The result is delivered to the corresponding component."
  builder_suggestions:
    kind: "query"
    place: "Page Server Component"
    origin_journey: "checkout"
    service: "getCheckoutShippingData(): Promise<CheckoutShippingData | null>"
    service_status: "not exposed"
    return_front_type: "CheckoutShippingData | null"
    return_front_type_status: "not exposed"
    details:
      - "Loader query executed on route entry in Next.js Server Component. getCheckoutShippingData is not exposed in apps/storefront/apis/index.ts."
```

```yaml
scenario:
  name: "Request save customer delivery address service"
  given:
    - "The buyer intends to save a new customer delivery address."
  when: "The component needs to invoke the save customer delivery address service."
  then:
    - "The save customer delivery address service is invoked."
    - "The updated delivery address book is returned."
    - "Confirmation or errors are delivered to the corresponding component."
  builder_suggestions:
    kind: "mutation"
    place: "Shell Client Component"
    origin_journey: "account"
    service: "saveDeliveryAddress(input: CustomerAddress): Promise<DeliveryAddressBook>"
    service_status: "exposed"
    return_front_type: "DeliveryAddressBook"
    return_front_type_status: "exposed"
    details:
      - "saveDeliveryAddress is directly exported in apps/storefront/apis/index.ts:31 (service_status: 'exposed'). DeliveryAddressBook is exported in apps/storefront/apis/domain.index.ts:40 (return_front_type_status: 'exposed')."
```

```yaml
scenario:
  name: "Request update current delivery address service"
  given:
    - "The buyer intends to set a delivery address as primary destination."
  when: "The component needs to invoke the update current delivery address service."
  then:
    - "The update current delivery address service is invoked."
    - "The updated delivery address book is returned."
    - "Confirmation or errors are delivered to the corresponding component."
  builder_suggestions:
    kind: "mutation"
    place: "Shell Client Component"
    origin_journey: "account"
    service: "updateCurrentDeliveryAddress(addressId: string): Promise<DeliveryAddressBook>"
    service_status: "exposed"
    return_front_type: "DeliveryAddressBook"
    return_front_type_status: "exposed"
    details:
      - "In apps/storefront/apis/index.ts:32, updateCurrentDeliveryAddress is already exported without an Action suffix (service_status: 'exposed'). DeliveryAddressBook is exported in domain.index.ts (return_front_type_status: 'exposed'). updateCurrentDeliveryAddress is the preferred exposed catalog service."
```

```yaml
scenario:
  name: "Request address autocomplete search service"
  given:
    - "The buyer intends to search for delivery address suggestions."
  when: "The component needs to invoke the address autocomplete search service."
  then:
    - "The address autocomplete search service is invoked."
    - "The address suggestions are returned."
    - "Confirmation or errors are delivered to the corresponding component."
  builder_suggestions:
    kind: "mutation"
    place: "Shell Client Component"
    origin_journey: "checkout"
    service: "searchAddressAutocomplete(query: string): Promise<AddressSuggestion[]>"
    service_status: "not exposed"
    return_front_type: "AddressSuggestion[]"
    return_front_type_status: "not exposed"
    details:
      - "Triggered on demand by client input in CheckoutShippingShell. Action suffix omitted. Neither service nor return type is exposed in storefront index catalogs."
```

### 2. Interactive Scenarios

```yaml
scenario:
  name: "Save customer delivery address"
  given:
    - "The buyer is on the delivery step."
    - "The buyer inputs a new valid address with district and street details."
  when:
    - "The buyer submits the address creation form."
  then:
    - "The address is created in the buyer account."
    - "If the operation results in error, an error message is displayed."
    - "If the operation succeeds and the current route is protected, the address is selected and the shell refreshes."
  builder_suggestions:
    place: "Shell Client Component"
    handler: "handleSaveAddress(address)"
    services:
      - "saveCustomerAddressAction(address)"
```

```yaml
scenario:
  name: "Set default delivery address"
  given:
    - "The buyer has multiple saved delivery addresses."
  when:
    - "The buyer marks an address as default."
  then:
    - "The address is designated as default in the buyer profile."
    - "If the operation results in error, an alert notification is shown."
    - "If the operation succeeds and the current route is protected, the default badge updates and the shell refreshes."
  builder_suggestions:
    place: "Shell Client Component"
    handler: "handleSetDefaultAddress(addressId)"
    services:
      - "setDefaultCustomerAddressAction(addressId)"
```

```yaml
scenario:
  name: "Search address autocomplete suggestions"
  given:
    - "The buyer enters an address search query with at least 3 characters."
  when:
    - "The search query input changes."
  then:
    - "Matching geocoded address suggestions are retrieved."
    - "If the operation results in error, an error state is handled gracefully."
    - "If the operation succeeds, the suggestion list is displayed to the buyer."
  builder_suggestions:
    place: "Shell Client Component"
    handler: "handleQueryChange(searchQuery)"
    services:
      - "searchAddressAutocompleteAction(searchQuery)"
```

| Behaviour Boundary | Scenario | Implementation suggestion |
| :--- | :--- | :--- |
| **Redirection** | **Unauthenticated access guard**<br/>**Given:** A guest visitor navigates to `/demo/checkout/delivery`.<br/>**When:** `getCheckoutShippingData()` returns null or session is missing.<br/>**Then:** The application redirects to `/login?from=/demo/checkout/delivery`. | Server Component guard: `redirect('/login?from=/demo/checkout/delivery')` |
| **Redirection** | **Bypass delivery guard when pickup-only**<br/>**Given:** All items across all seller groups are configured for store pickup (`requiresShippingAddress: false`).<br/>**When:** The delivery route initializes.<br/>**Then:** The application forwards the buyer directly to `/demo/checkout/payment`. | Server Component / Shell guard: `redirect('/demo/checkout/payment')` |
| **Redirection** | **Missing personal draft guard**<br/>**Given:** The buyer visits delivery without completing personal details.<br/>**When:** The delivery route evaluates personal draft completeness.<br/>**Then:** The application redirects back to `/demo/checkout`. | Route guard / Shell check: `router.push('/demo/checkout')` |
| **Redirection** | **Display error screen on shipping data read failure**<br/>**Given:** An authenticated buyer navigates to `/demo/checkout/delivery`.<br/>**When:** The shipping service throws an unhandled exception.<br/>**Then:** The application renders the system error screen. | Automatic Next.js error boundary (`error.tsx`) |
| **Local State** | **Toggle fulfillment method per seller**<br/>**Given:** The cart contains items from one or more sellers.<br/>**When:** The buyer toggles between Delivery and Recojo for a store.<br/>**Then:** The shell updates `fulfillmentGroups`, re-evaluates `requiresShippingAddress`, and toggles store pickup location selector. | Shell state: `handleFulfillmentMethodChange` updating `shippingData` |
| **Local State** | **Select pickup location per store**<br/>**Given:** Recojo en tienda is selected for a store.<br/>**When:** The buyer selects a store branch from the location dropdown.<br/>**Then:** The shell updates `selectedPickupLocationId` for that seller group. | Shell state: `handlePickupLocationChange` |
| **Local State** | **Select saved delivery address**<br/>**Given:** Saved addresses are displayed.<br/>**When:** The buyer selects an address card.<br/>**Then:** The shell updates `selectedAddressId` and marks it as default via transition. | Shell state: `handleSelectedAddressChange` |
| **Local State** | **Interactive map pin placement**<br/>**Given:** The interactive map modal is open.<br/>**When:** The buyer repositions the location pin.<br/>**Then:** The shell updates coordinate draft and reverse-geocoded address. | Shell state: map coordinate state updating address draft |
| **Local State** | **Step progression to payment**<br/>**Given:** Valid shipping address or pickup locations are configured.<br/>**When:** The buyer clicks "Ir a pagar".<br/>**Then:** The shell transitions to the payment step. | Client transition: `router.push('/demo/checkout/payment')` |

### 3. Declarative (NO-OP) Scenarios

| Behaviour Boundary | Scenario | Implementation suggestion |
| :--- | :--- | :--- |
| **Navigation** | **Back to personal data step**<br/>**Given:** The buyer is on the delivery step.<br/>**When:** The buyer clicks the back button in the header.<br/>**Then:** The buyer is navigated back to the personal information step. | Link destination pattern: `href: /demo/checkout` (via header `onBack` or `<Link>`) |
| **Navigation** | **Delivery policies and coverage link navigation**<br/>**Given:** The buyer reviews delivery rates and shipping zones.<br/>**When:** The buyer clicks the delivery coverage or shipping policy link.<br/>**Then:** The buyer is navigated to the delivery information view. | Static link destination: `href: /shipping-policy` |

---

## Route: `/demo/checkout/payment` (Payment and Order Authorization)

### 1. Service Operations (`apps/storefront/apis`)

```yaml
scenario:
  name: "Retrieve buyer profile for payment context"
  given:
    - "An authenticated buyer accesses the payment step (/demo/checkout/payment)."
  when: "The component executes the service call."
  then:
    - "The buyer personal profile and shipping selections are retrieved."
    - "The result is delivered to the corresponding component."
  builder_suggestions:
    kind: "query"
    place: "Page Server Component"
    origin_journey: "checkout"
    service: "getCheckoutPersonalData(): Promise<CheckoutPersonalData | null>"
    service_status: "not exposed"
    return_front_type: "CheckoutPersonalData | null"
    return_front_type_status: "not exposed"
```

```yaml
scenario:
  name: "Retrieve shipping fulfillment choices for payment context"
  given:
    - "The payment route prepares the checkout draft."
  when: "The component executes the service call."
  then:
    - "The shipping address and store fulfillment selections are retrieved."
    - "The result is delivered to the corresponding component."
  builder_suggestions:
    kind: "query"
    place: "Page Server Component"
    origin_journey: "checkout"
    service: "getCheckoutShippingData(): Promise<CheckoutShippingData | null>"
    service_status: "not exposed"
    return_front_type: "CheckoutShippingData | null"
    return_front_type_status: "not exposed"
```

```yaml
scenario:
  name: "Retrieve prepared checkout and payment quote"
  given:
    - "The buyer arrives at the payment step with validated personal and fulfillment data."
  when: "The component executes the service call."
  then:
    - "The authoritative cart summary, revalidation status, and payment quote are retrieved."
    - "The result is delivered to the corresponding component."
  builder_suggestions:
    kind: "query"
    place: "Page Server Component"
    origin_journey: "checkout"
    service: "prepareCheckout(input): Promise<PreparedCheckout>"
    service_status: "exposed"
    return_front_type: "PreparedCheckout"
    return_front_type_status: "not exposed"
    details:
      - "prepareCheckout is exposed in apps/storefront/apis/index.ts:69 under use cases (service_status: 'exposed'). PreparedCheckout is not in apps/storefront/apis/domain.index.ts (return_front_type_status: 'not exposed')."
```

```yaml
scenario:
  name: "Request prepare checkout quote service"
  given:
    - "The buyer intends to refresh or re-prepare an expired payment quote."
  when: "The component needs to invoke the prepare checkout quote service."
  then:
    - "The prepare checkout quote service is invoked."
    - "The prepared checkout snapshot is returned."
    - "Confirmation or errors are delivered to the corresponding component."
  builder_suggestions:
    kind: "mutation"
    place: "Shell Client Component"
    origin_journey: "checkout"
    service: "prepareCheckout(input): Promise<CheckoutActionResult<PreparedCheckout>>"
    service_status: "exposed"
    return_front_type: "CheckoutActionResult<PreparedCheckout>"
    return_front_type_status: "not exposed"
    details:
      - "Action suffix stripped. Matches exposed catalog export prepareCheckout (service_status: 'exposed')."
```

```yaml
scenario:
  name: "Request complete checkout and payment service"
  given:
    - "The buyer intends to complete checkout and authorize payment."
  when: "The component needs to invoke the complete checkout and payment service."
  then:
    - "The complete checkout and payment service is invoked."
    - "The order confirmation result is returned."
    - "The canonical cart and checkout cache paths are revalidated."
    - "Confirmation or errors are delivered to the corresponding component."
  builder_suggestions:
    kind: "mutation"
    place: "Shell Client Component"
    origin_journey: "checkout"
    service: "completeCheckout(input, attemptId, payment): Promise<CheckoutActionResult<CheckoutOrderResult>>"
    service_status: "exposed"
    return_front_type: "CheckoutActionResult<CheckoutOrderResult>"
    return_front_type_status: "not exposed"
    details:
      - "Action suffix stripped from completeCheckoutAction. Matches exposed use case export completeCheckout in apps/storefront/apis/index.ts:67 (service_status: 'exposed')."
```

### 2. Interactive Scenarios

```yaml
scenario:
  name: "Complete order purchase"
  given:
    - "The buyer has selected an available payment method."
    - "A valid signed quote and attempt identifier are active."
  when:
    - "The buyer clicks the pay button."
  then:
    - "The payment is processed and order record created."
    - "If the operation results in error, the payment lifecycle transitions to declined and feedback is shown."
    - "If the operation succeeds and the current route is protected, the buyer is redirected to the order confirmation route."
  builder_suggestions:
    place: "Shell Client Component"
    handler: "handlePay()"
    services:
      - "prepareCheckoutAction(input)"
      - "completeCheckoutAction(input, attemptId, payment)"
```

| Behaviour Boundary | Scenario | Implementation suggestion |
| :--- | :--- | :--- |
| **Redirection** | **Unauthenticated access guard**<br/>**Given:** A guest visitor navigates to `/demo/checkout/payment`.<br/>**When:** `getCheckoutPersonalData()` returns null.<br/>**Then:** The application redirects immediately to `/login?from=/demo/checkout/payment`. | Server Component guard: `redirect('/login?from=/demo/checkout/payment')` |
| **Redirection** | **Prerequisites incomplete guard**<br/>**Given:** Personal draft is incomplete, shipping address is missing when required, or cart is empty.<br/>**When:** Payment route initializes.<br/>**Then:** The application redirects the buyer to the earliest incomplete step (`/demo/cart`, `/demo/checkout`, or `/demo/checkout/delivery`). | Route guard / loader check: `redirect('/demo/checkout')` or `redirect('/demo/cart')` |
| **Redirection** | **Order completion confirmation redirection**<br/>**Given:** `completeCheckoutAction()` succeeds with status ok.<br/>**When:** Payment charge is authorized and order number is generated.<br/>**Then:** The buyer is redirected to the order confirmation view `/demo/orders/${order_number}?placed=1`. | Client redirection: `router.push('/demo/orders/' + order_number + '?placed=1')` |
| **Redirection** | **Display error screen on payment preparation failure**<br/>**Given:** An unhandled error occurs during payment preparation.<br/>**When:** The Server Component executes `prepareCheckout`.<br/>**Then:** The application renders the system error screen. | Automatic Next.js error boundary (`error.tsx`) |
| **Local State** | **Select payment method card**<br/>**Given:** Available payment methods (Tarjeta, Yape, Plin) are displayed.<br/>**When:** The buyer clicks a payment method card.<br/>**Then:** The shell updates `selectedMethodId` and highlights the active method. | Shell state: `setSelectedMethodId(methodId)` |
| **Local State** | **Payment lifecycle progression**<br/>**Given:** The buyer initiates purchase payment.<br/>**When:** Gateway communication and authorization execute.<br/>**Then:** The shell transitions `lifecycle` state (`idle` -> `opening` -> `submitting` -> `paid` / `declined` / `unavailable`). | Shell state: `useState<CheckoutPaymentLifecycle>('idle')` / `setLifecycle` |
| **Local State** | **Handle cart revalidation change notice**<br/>**Given:** Price or inventory changed while preparing payment.<br/>**When:** `prepareCheckout` detects adjustments.<br/>**Then:** The shell displays a warning notice detailing cart adjustments and prompts the buyer to review. | Shell state: `lifecycle = 'quote_changed'` with warning banner |
| **Local State** | **Handle expired payment quote**<br/>**Given:** The 15-minute signed payment quote expires.<br/>**When:** The buyer attempts payment or the timer elapses.<br/>**Then:** The shell prompts the buyer to refresh the quote before finalizing purchase. | Shell state: quote refresh trigger invoking `prepareCheckoutAction` |

### 3. Declarative (NO-OP) Scenarios

| Behaviour Boundary | Scenario | Implementation suggestion |
| :--- | :--- | :--- |
| **Navigation** | **Back from payment to previous step**<br/>**Given:** The buyer is on the payment method step.<br/>**When:** The buyer clicks the back arrow in the header.<br/>**Then:** The buyer is navigated to `/demo/checkout/delivery` if shipping was required, or `/demo/checkout` if pickup-only. | Conditional navigation link pattern: `href: /demo/checkout/delivery` or `href: /demo/checkout` (via header `onBack` or `<Link>`) |
| **Navigation** | **Payment security and terms link navigation**<br/>**Given:** The buyer inspects payment gateway security badges.<br/>**When:** The buyer clicks the payment terms or security guarantee link.<br/>**Then:** The buyer is navigated to the payment terms information page. | Static link destination: `href: /terms/payments` |
| **Navigation** | **Refund and cancellation policy navigation**<br/>**Given:** The buyer reviews order conditions before purchase.<br/>**When:** The buyer clicks the refund policy link.<br/>**Then:** The buyer is navigated to the cancellation and refund policy page. | Static link destination: `href: /returns` |

---

## Design Notes

- **Shared Transactional Layout Isolation**: The Transactional Commerce Layout (`apps/storefront/src/app/demo/(commerce)/layout.tsx`) wraps both the cart and checkout journeys under the `(commerce)` route group. This architecture strips the universal storefront header (removing search bars, categories menu, and catalog navigation) to minimize buyer distraction and funnel abandonment, providing a dedicated transactional canvas.
- **Route vs Shell Boundary Enforcement**: Data loading (`getCheckoutPersonalData`, `getCheckoutShippingData`, `prepareCheckout`) is executed by Next.js Server Components on each specific checkout route page. Shell components (`CheckoutPersonalDataShell`, `CheckoutShippingShell`, `CheckoutPaymentShell`) handle localized UI state, transition feedback, and trigger Server Actions (`saveBuyerFiscalIdentityAction`, `saveCustomerAddressAction`, `setDefaultCustomerAddressAction`, `searchAddressAutocompleteAction`, `prepareCheckoutAction`, `completeCheckoutAction`).
- **Domain Contract Compliance**: All service signatures and returned front types align strictly with `apps/storefront/apis/checkout/domain/contracts/checkout.contract.ts` and `apps/storefront/apis/checkout/application/actions/checkout.action.ts`.
- **Pure Link Categorization**: All static and back-navigation links are categorized under Declarative (NO-OP) Scenarios, isolating them from technical implementation and mutation workflows.
- **Separation of Concerns**: Data DTO tables and schemas are omitted in accordance with specification standards; data models belong exclusively to `design-journey-data-model`.

## Focused Refinement Questions

- None. All service operations, domain contracts, and interaction boundaries have been validated against the implementation in `apps/storefront/apis/checkout/` and `apps/storefront/src/app/demo/(commerce)/checkout/`.
