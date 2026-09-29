# Use Cases - `store`

## Route: `/store/[slug]`

### 1. Service Operations (`apps/storefront/apis`)

| Scenario | Service Call | Returned Front Type | Implementation Suggestion | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Obtener perfil público de la tienda**<br/>**Given:** Un slug de tienda válido `slug`.<br/>**When:** La página de tienda es solicitada en el servidor.<br/>**Then:** Resuelve el contrato de datos del perfil gobernado (`PublicStoreProfile`), incluyendo insignias de verificación y enlace comunitario seguro. | `storeApi.getPublicStoreProfile(slug)` | `PublicStoreProfile` | Ejecutar en paralelo dentro de `Promise.all` en el Server Component (`page.tsx`) vía `@chiki/search` / Postgres RPC `get_public_store_profile`. | |
| **Listar catálogo público de la tienda**<br/>**Given:** Un slug de tienda válido `slug` y un número de página opcional `page`.<br/>**When:** La página de tienda es solicitada en el servidor.<br/>**Then:** Resuelve los ítems de catálogo paginados (`PublicStoreCatalogResponse`) con ofertas recomendadas, rangos de precio e indicadores de stock. | `storeApi.listPublicStoreCatalog(slug, page)` | `PublicStoreCatalogResponse` | Ejecutar concurrentemente en `page.tsx` (`PAGE_SIZE = 24`, sobre-consulta +1 para resolver `hasNextPage`) vía `@chiki/search` / Postgres RPC `list_public_store_catalog`. | |

### 2. Page & Interaction Behaviors

| Scenario | Behavior Boundary | Implementation Suggestion | Status |
| :--- | :--- | :--- | :--- |
| **Preservación de cabecera universal**<br/>**Given:** El usuario navega hacia `/store/[slug]`.<br/>**When:** Se renderiza la página.<br/>**Then:** La cabecera universal con barra de navegación, búsqueda y acceso a carrito se mantiene visible y funcional como parte de la experiencia consistente de storefront. | Navigation / Layout | Renderizado continuo del layout universal (`CartHeader` / barra de navegación global). | |
| **Tienda inexistente o inactiva**<br/>**Given:** Un slug de tienda que no existe en el sistema o la tienda tiene estado inactivo/suspendido.<br/>**When:** Se procesa la solicitud de la página.<br/>**Then:** La ruta invoca inmediatamente `notFound()` mostrando la pantalla estándar 404. | Route Guard / Boundary | Invocación a `notFound()` de Next.js al evaluar `!profileResult.profile`. | |
| **Error de carga de perfil de tienda**<br/>**Given:** Falla la ejecución de la consulta RPC `get_public_store_profile`.<br/>**When:** La página intenta renderizar.<br/>**Then:** Renderiza la vista de error `StoreProfileLoadError` con encabezado, mensaje descriptivo de reintento en unos minutos y botón hacia `/catalog`. | Error Boundary | Componente `StoreProfileLoadError` con `Callout variant="danger"` y `ActionButton href="/catalog"`. | |
| **Catálogo no disponible o degradado**<br/>**Given:** El perfil de la tienda carga exitosamente pero `listPublicStoreCatalog` falla con error de red o base de datos.<br/>**When:** La página renderiza el perfil.<br/>**Then:** El perfil de tienda (avatar, nombre, descripción, badges, quick links) se muestra intacto y la sección `#productos` renderiza un Callout de error sin romper la navegación. | Degraded State | Inyección de `catalog.error = 'No pudimos cargar los productos. Inténtalo nuevamente.'` y `items: []` en `StoreProfileScreen`. | |
| **Navegación y paginación del catálogo**<br/>**Given:** La tienda tiene más de 24 productos (`hasNextPage` es true o `currentPage > 1`).<br/>**When:** El usuario hace clic en los enlaces de paginación "Anterior" o "Siguiente".<br/>**Then:** La navegación traslada a `/store/[slug]?page=[N]` preservando el estado de paginación. | Navigation | Renderizado de enlaces semánticos `previousHref` y `nextHref` calculados mediante `storePageHref(slug, page)`. | |
| **Navegación a producto con preservación de contexto de listing**<br/>**Given:** El usuario selecciona un ítem en la cuadrícula de catálogo de la tienda.<br/>**When:** Se hace clic en la tarjeta del producto.<br/>**Then:** Navega a `/catalog/[slug]?listing=[recommendedListingId]` permitiendo al PDP preseleccionar la oferta de esta tienda. | Navigation | Mapeado de enlaces vía `toPublicStoreCatalogGridItems` inyectando query parameter `?listing=`. | |
| **CTA "Comprar en esta tienda" (scroll suave)**<br/>**Given:** La tienda cuenta con catálogo de productos disponible en la página.<br/>**When:** El usuario activa el enlace "Ver productos de esta tienda" / CTA en `StoreProfileHero`.<br/>**Then:** La vista realiza un scroll suave hacia el contenedor ancla `#productos`. | Local Interaction | Enlace de anclaje `ctaHref="#productos"` con navegación intra-página sin recarga. | |
| **Enlace rápido a comunidad externa**<br/>**Given:** La tienda tiene configurado un enlace válido con protocolo `https://` en `community_link`.<br/>**When:** El usuario hace clic en la píldora "Comunidad".<br/>**Then:** Se abre el enlace externo validado (ej. WhatsApp, Discord, Telegram). | External Navigation | Sanitización mediante `publicStoreCommunityHref` y renderizado en `quickLinks` de `StoreProfileHero`. | |

---

## Design notes

- **Transport Agnostic Domain:** Las operaciones bajo `Service Operations` definen capacidades de lectura del storefront (`apps/storefront/apis` / `@chiki/search`), resolviendo directamente los tipos del Data Model sin atarse prematuramente a la infraestructura de red.
- **Governed Public Data:** Las consultas de perfil y catálogo respetan estrictamente los límites de confianza de Supabase (`anon` key / publishable role) mediante RPCs seguras (`get_public_store_profile`, `list_public_store_catalog`), omitiendo información privada de membresías o identificadores internos de Medusa.
- **Parallel Query Execution:** En la carga inicial de `/store/[slug]`, las consultas de perfil y catálogo se ejecutan concurrentemente con `Promise.all` para optimizar el tiempo de respuesta inicial (TTFB).
- **Graceful Partial Failure:** Si el catálogo de la tienda falla, el perfil de la tienda se mantiene visible y accesible, evitando fallos catastróficos de página completa ante degradaciones parciales del servicio de búsqueda.
