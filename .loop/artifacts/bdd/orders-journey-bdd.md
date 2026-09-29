# Use Cases - `orders`

## Server Component Scenarios

### Route: `/demo/orders`

| Scenario | Type | Status |
| :--- | :--- | :--- |
| **Load customer order history**<br/>**Given:** An authenticated buyer accesses `/demo/orders`.<br/>**When:** The page executes `getMyOrders(userId)`.<br/>**Then:** Returns sorted order rows with multi-merchant previews, aggregated status, and total amount. | Call | Proposed |
| **Pre-render empty history state**<br/>**Given:** Authenticated user has zero lifetime orders.<br/>**When:** `getMyOrders` resolves with an empty collection.<br/>**Then:** Passes empty orders array and default label "Todavía no tienes pedidos." to `OrderHistoryScreen`. | Composition | Proposed |
| **Handle orders service downtime**<br/>**Given:** Supabase connection fails or orders table is temporarily unreachable.<br/>**When:** `getMyOrders` throws `orders_unavailable`.<br/>**Then:** Returns `OrderHistoryScreen` with danger Callout notice ("Historial no disponible. Inténtalo nuevamente en unos minutos."). | Branch | Proposed |

### Route: `/demo/orders/[orderNumber]`

| Scenario | Type | Status |
| :--- | :--- | :--- |
| **Load complete order detail**<br/>**Given:** An authenticated buyer accesses `/demo/orders/[orderNumber]`.<br/>**When:** `getMyOrderByNumber(orderNumber, userId)` executes.<br/>**Then:** Returns complete order graph: buyer snapshot, shipping address, seller groups, items, and comprobantes. | Call | Proposed |
| **Protect unauthorized or missing order**<br/>**Given:** `orderNumber` does not exist or belongs to another user account.<br/>**When:** `getMyOrderByNumber` returns null.<br/>**Then:** Triggers Next.js `notFound()` without exposing internal existence or authorization details. | Branch | Proposed |
| **Handle order query read failure**<br/>**Given:** Database read throws an unexpected query error.<br/>**When:** Try/catch captures `order_unavailable`.<br/>**Then:** Returns `OrderHistoryScreen` with danger Callout notice ("Pedido no disponible. Inténtalo nuevamente en unos minutos."). | Branch | Proposed |
| **Display post-checkout confirmation banner**<br/>**Given:** Buyer completes checkout and is redirected with query `?placed=1`.<br/>**When:** Order detail screen initializes.<br/>**Then:** Renders green success Callout banner ("¡Gracias por tu compra! Tu pedido fue creado correctamente."). | Composition | Proposed |

---

## Actions Scenarios

### Route: `/demo/orders`

| Scenario | Type | Status |
| :--- | :--- | :--- |
| **Unauthenticated access guard**<br/>**Given:** A visitor without an active session requests `/demo/orders`.<br/>**When:** `getCurrentUser()` returns null.<br/>**Then:** Redirects immediately to `/login?from=/demo/orders`. | Client guard | Proposed |

### Route: `/demo/orders/[orderNumber]`

| Scenario | Type | Status |
| :--- | :--- | :--- |
| **Unauthenticated access guard**<br/>**Given:** A visitor without an active session requests `/demo/orders/[orderNumber]`.<br/>**When:** `getCurrentUser()` returns null.<br/>**Then:** Redirects immediately to `/login?from=/demo/orders/[orderNumber]`. | Client guard | Proposed |
| **Submit customer satisfaction rating**<br/>**Given:** Delivered order has no existing rating (`rating.score === null`).<br/>**When:** User clicks star rating (1-5 stars) on `OrderRatingPanel`.<br/>**Then:** Invokes Server Action persisting rating score and updates display message to "¡Gracias por calificar !". | Server Action | Proposed |

---

## Navigation Scenarios

### Route: `/demo/orders`

| Scenario | Type | Status |
| :--- | :--- | :--- |
| **Navigate to order detail**<br/>**Given:** User is viewing the order history card grid.<br/>**When:** User clicks an individual `OrderCard`.<br/>**Then:** Navigates client router to `/demo/orders/[orderNumber]`. | Navigation | Proposed |
| **Close order history**<br/>**Given:** User is viewing `/demo/orders`.<br/>**When:** User activates the header close 'X' button.<br/>**Then:** Navigates back to `/demo/account`. | Navigation | Proposed |

### Route: `/demo/orders/[orderNumber]`

| Scenario | Type | Status |
| :--- | :--- | :--- |
| **Back to order history**<br/>**Given:** User is viewing order detail.<br/>**When:** User clicks the back arrow `< Detalle de pedido`.<br/>**Then:** Navigates back to `/demo/orders`. | Navigation | Proposed |
| **Real-time courier tracking navigation**<br/>**Given:** Order contains active courier dispatch info (`tracking !== null`).<br/>**When:** User clicks "Trackear envío" link.<br/>**Then:** Opens carrier logistics tracking portal in a new browser tab. | Navigation | Proposed |
| **Download SUNAT comprobante PDF**<br/>**Given:** Order has an issued comprobante with `status === 'accepted'` and valid `pdfUrl`.<br/>**When:** User clicks "Descargar" in Comprobantes section.<br/>**Then:** Opens official SUNAT PDF document in a new browser tab. | Navigation | Proposed |
| **Navigate to product catalog from line item**<br/>**Given:** Order detail lists purchased card items.<br/>**When:** User clicks a card listing title or artwork.<br/>**Then:** Navigates to corresponding product catalog page. | Navigation | Proposed |

---

## Local Scenarios

### Route: `/demo/orders`

| Scenario | Type | Status |
| :--- | :--- | :--- |
| **Dim cancelled order previews**<br/>**Given:** An order card has status `cancelled`.<br/>**When:** Card artwork previews render.<br/>**Then:** Applies CSS `opacity-40 saturate-50` to visually attenuate cancelled item artwork. | Local | Proposed |
| **Calculate overlapping card offset**<br/>**Given:** Order body renders up to 8 card art previews.<br/>**When:** Container width is measured via `ResizeObserver`.<br/>**Then:** Dynamically computes horizontal step offset (`getCardLeft`) to produce fan stack effect. | Local | Proposed |

### Route: `/demo/orders/[orderNumber]`

| Scenario | Type | Status |
| :--- | :--- | :--- |
| **Interactive star rating selection**<br/>**Given:** Delivered order has not yet been rated (`readOnly === false`).<br/>**When:** User hovers or taps on star icons (1 to 5).<br/>**Then:** Updates active filled star count and accessibility label ("X de 5"). | Local | Proposed |
| **Render multi-seller fulfillment sections**<br/>**Given:** Order contains items fulfilled by multiple stores.<br/>**When:** Order detail renders.<br/>**Then:** Renders distinct article containers for each store with fulfillment method badge ('Recojo en tienda' vs 'Delivery') and specific shipping/pickup addresses. | Local | Proposed |
| **Comprobante lifecycle status presentation**<br/>**Given:** Order has electronic invoicing document in progress or completed.<br/>**When:** Documents section renders.<br/>**Then:** Renders contextual Callout: green success with "Descargar" button if `accepted`, blue info if `submitted`/validating, neutral if `pending`, and yellow warning if `anulacionStatus` is in-flight. | Local | Proposed |

---

## Design notes

- **Authentication Enforcement**: Both `/demo/orders` and `/demo/orders/[orderNumber]` strictly require an authenticated session. Unauthenticated access is redirected to `/login?from=<route>`.
- **Order Isolation & RLS Security**: `getMyOrderByNumber` strictly filters by both `order_number` and `user_id`. Non-matching orders fail closed as `notFound()`, preventing enumeration or metadata leakage across buyers.
- **Multi-Merchant Order Grouping**: Orders are partitioned by seller store (`sellerGroups`), supporting mixed fulfillment orders split between different merchants (e.g., store pickup from 'ChikiArena' and home delivery from 'Otra empresa').
- **Immutable Snapshots**: Line items (`seller_order_items`), buyer identity (`order_buyer_snapshots`), and shipping addresses (`order_shipping_address_snapshots`) freeze historical purchase data, ensuring past orders remain immutable regardless of catalog or address book changes.
- **SUNAT Comprobante Issuance**: Electronic receipts (boletas and facturas) are issued asynchronously by Chiki Arena as Merchant of Record, providing direct PDF download links once confirmed by SUNAT (`status === 'accepted'`).
- **UI Mockup Field Preservation**: In accordance with domain rules, visually present mockup elements—including live courier tracking (`tracking`), post-purchase star rating (`rating`), and delivered date timestamp (`deliveredDate`)—are preserved as nullable types with explicit backend implementation notes.
