# Use Cases - `account`

## Route: `/account`

### 1. Service Operations (`apps/storefront/apis`)

| Scenario | Service Call | Returned Front Type | Implementation Suggestion | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Obtener perfil del comprador**<br/>**Given:** Existe una sesión de usuario activa en el servidor.<br/>**When:** Se invoca la operación de lectura de perfil.<br/>**Then:** Resuelve los datos de identidad y teléfono del comprador. | `accountApi.getAccountProfile()` | `AccountProfile` | Ejecutar en paralelo en Server Component (`page.tsx`). | |
| **Resiliencia ante perfil inexistente (Graceful Fallback)**<br/>**Given:** Usuario autenticado en Auth pero sin fila en `user_profiles`.<br/>**When:** Se invoca la lectura de perfil.<br/>**Then:** Retorna un `AccountProfile` provisional derivado del email con campos nulos sin romper la renderización. | `accountApi.getAccountProfile()` | `AccountProfile` | Aislar la lógica de fallback defensivo dentro del repositorio/servicio. | |
| **Actualizar datos del perfil**<br/>**Given:** El usuario envía cambios en nombre, documento o teléfono.<br/>**When:** Se confirma la actualización de datos personales.<br/>**Then:** Persiste los cambios en `user_profiles` y retorna el `AccountProfile` actualizado. | `accountApi.updateAccountProfile(input)` | `AccountProfile` | Exponer como Server Action y revalidar `/account`. | |
| **Obtener libro de direcciones de entrega**<br/>**Given:** Usuario autenticado con o sin direcciones registradas.<br/>**When:** Se consultan las direcciones guardadas.<br/>**Then:** Resuelve la lista ordenada (predeterminada primero) y el total de direcciones. | `addressApi.getCustomerAddressBook()` | `CustomerAddressBook` | Ejecutar concurrentemente en `page.tsx` dentro de `Promise.all`. | |
| **Establecer dirección predeterminada**<br/>**Given:** El usuario tiene múltiples direcciones registradas.<br/>**When:** Selecciona una dirección para marcarla como predeterminada.<br/>**Then:** Adquiere bloqueo transaccional, actualiza `isDefault` y retorna el libro sincronizado. | `addressApi.setDefaultCustomerAddress(addressId)` | `CustomerAddressBook` | Exponer como Server Action invocando `set_default_customer_address` RPC. | |
| **Eliminar dirección guardada**<br/>**Given:** El usuario solicita eliminar una dirección.<br/>**When:** Se confirma la eliminación de la tarjeta.<br/>**Then:** Remueve el registro y retorna el `CustomerAddressBook` actualizado. | `addressApi.deleteCustomerAddress(addressId)` | `CustomerAddressBook` | Exponer como Server Action invocando `delete_customer_address` RPC. | |
| **Obtener identidades de facturación electrónica**<br/>**Given:** Usuario autenticado con o sin comprobantes registrados.<br/>**When:** Se consultan las identidades fiscales disponibles.<br/>**Then:** Resuelve las identidades guardadas (Boleta/Factura) y el ID del comprobante predeterminado. | `fiscalApi.getBuyerFiscalIdentitiesBook()` | `BuyerFiscalIdentitiesBook` | Ejecutar concurrentemente en `page.tsx`. | |
| **Guardar / Actualizar identidad fiscal (SUNAT)**<br/>**Given:** Datos de comprobante válidos (DNI 8 dígitos, RUC 11 dígitos, nombre/razón social).<br/>**When:** Se envía el formulario de facturación.<br/>**Then:** Persiste la plantilla en `buyer_fiscal_identities` y retorna el `BuyerFiscalIdentitiesBook` actualizado, desmarcando otras si se marcó como default. | `fiscalApi.saveBuyerFiscalIdentity(input)` | `BuyerFiscalIdentitiesBook` | Exponer como Server Action consumido por el modal de facturación. | |
| **Establecer identidad fiscal predeterminada**<br/>**Given:** Múltiples identidades registradas en el libro fiscal.<br/>**When:** Se marca una identidad como favorita/predeterminada.<br/>**Then:** Actualiza `is_default = true`, apaga el flag en las demás y retorna el libro sincronizado. | `fiscalApi.setDefaultBuyerFiscalIdentity(identityId)` | `BuyerFiscalIdentitiesBook` | Exponer como Server Action liviano para selector de tarjeta. | |
| **Eliminar identidad fiscal**<br/>**Given:** Una identidad fiscal existente registrada.<br/>**When:** Se confirma la eliminación de la tarjeta.<br/>**Then:** Remueve el registro en base de datos y retorna el libro actualizado. | `fiscalApi.deleteBuyerFiscalIdentity(identityId)` | `BuyerFiscalIdentitiesBook` | Exponer como Server Action llamando a `delete_buyer_fiscal_identity`. | |

### 2. Page & Interaction Behaviors

| Scenario | Behavior Boundary | Implementation Suggestion | Status |
| :--- | :--- | :--- | :--- |
| **Bloqueo de acceso y redirección a login**<br/>**Given:** Visitante sin sesión activa intenta acceder a `/account`.<br/>**When:** Se evalúa el guard de autenticación.<br/>**Then:** Interrumpe la renderización y redirige a `/login?redirect=/account`. | Guard / Redirect | Implementar en el nivel más alto (`page.tsx` o `layout.tsx`) antes de consultar APIs. | |
| **Alternar tipo de comprobante en formulario (Personal vs Empresa)**<br/>**Given:** Usuario con modal de facturación abierto.<br/>**When:** Conmuta el selector entre "Personal" y "Empresa".<br/>**Then:** El formulario conmuta reglas: fija tipo RUC (11 dígitos) y solicita Razón Social para Empresa; habilita DNI/CE para Personal. | Local Form | Estado puramente local (`useState` o reducer) dentro del modal. | |
| **Selección optimista de comprobante predeterminado**<br/>**Given:** Usuario visualiza la lista de comprobantes guardados.<br/>**When:** Hace clic en el switch o selector "Usar como comprobante predeterminado".<br/>**Then:** La UI actualiza inmediatamente la insignia de predeterminada y despacha la mutación al servidor en segundo plano; revierte en caso de fallo. | Optimistic Update | Implementar con `useOptimistic` en el Client Shell (`account-client.tsx`) o componente de tarjeta. | |
| **Cerrar sesión de cuenta**<br/>**Given:** Usuario con sesión activa en `/account`.<br/>**When:** Selecciona la acción "Cerrar sesión".<br/>**Then:** Invoca `signOut` en el cliente de autenticación, destruye cookies de sesión y redirige a `/`. | Action / Redirect | Ejecutar desde el botón de logout en el footer/session bar. | |

---

## Route: `/account/addresses`

### 1. Service Operations (`apps/storefront/apis`)

| Scenario | Service Call | Returned Front Type | Implementation Suggestion | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Guardar nueva dirección con validación de Ubigeo nacional**<br/>**Given:** Formulario completado con departamento, provincia, distrito, ubigeo de 6 dígitos y teléfono.<br/>**When:** Se confirma el guardado de la dirección.<br/>**Then:** Valida los estándares logísticos nacionales, persiste vía RPC y retorna el `CustomerAddressBook` actualizado. | `addressApi.saveCustomerAddress(input)` | `CustomerAddressBook` | Exponer como Server Action con redirección de regreso a `/account`. | |

### 2. Page & Interaction Behaviors

| Scenario | Behavior Boundary | Implementation Suggestion | Status |
| :--- | :--- | :--- | :--- |
| **Validación de campos obligatorios en formulario**<br/>**Given:** Usuario completando el formulario de dirección.<br/>**When:** Modifica los campos de dirección y destinatario.<br/>**Then:** Valida en tiempo real que el ubigeo tenga 6 dígitos y el teléfono cumpla formato peruano antes de habilitar el submit. | Local Form | Validación en cliente vía hook de formulario (`react-hook-form` / Zod). | |
| **Volver a la vista principal de cuenta**<br/>**Given:** Usuario en `/account/addresses`.<br/>**When:** Presiona el botón de volver o la navegación superior.<br/>**Then:** Navega de regreso a `/account` preservando el estado de la sesión. | Navigation | Enlace estándar Next.js `<Link href="/account">`. | |

---

## Design notes

- **Transport Agnostic Domain:** Las operaciones bajo `Service Operations` definen capacidades puras de la API de storefront (`apps/storefront/apis`), resolviendo o mutando directamente los front types del Data Model sin atarse prematuramente a Server Actions o llamadas directas en componentes.
- **Atomic Default Guarantees:** Las operaciones de asignación predeterminada (`setDefaultCustomerAddress` y `setDefaultBuyerFiscalIdentity`) garantizan atómicamente la exclusividad del flag `isDefault = true` para el usuario mediante procedimientos transaccionales.
- **Parallel Query Execution:** En la carga inicial de `/account`, las tres operaciones de lectura (`getAccountProfile`, `getCustomerAddressBook` y `getBuyerFiscalIdentitiesBook`) deben orquestarse concurrentemente para prevenir cascadas de red.
- **Client-Side Derivation Boundary:** Lógicas puramente visuales y dinámicas (como el cálculo relativo de fechas o insignias de estado) se mantienen como responsabilidades de presentación en el Screen Component.

## Focused refinement questions

- ¿Se requerirá en el futuro un buscador de direcciones basado en autocompletado de mapas (Google Maps / Mapbox) o la selección manual por ubigeo satisface la etapa actual?
- ¿El modal de edición de perfil debe permitir la desvinculación o modificación del número de documento una vez emitido el primer comprobante fiscal formal?
