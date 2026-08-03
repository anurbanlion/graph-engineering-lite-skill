# Resumen de Jobs

### 1. `analyze-journey-use-cases`
* **Objetivo:** Clasificar casos de uso UI en pages y shells, y mapear la implementación existente vs esperada.
* **Input:** Nombre de `domain`, archivos o código de página y shell, capturas de pantalla o descripción del flujo UI.
* **Output:** Documento Markdown con tablas de casos de uso esperados (`🎯`), existentes (`🔎`) y excluidos.

---

### 2. `compile-storefront-journeys`
* **Objetivo:** Compilar e identificar los *journeys* existentes en la aplicación desde el directorio de ejecuciones (*runs*).
* **Input:** Nombre de `domain` (por defecto `global-designs`).
* **Output:** Documento Markdown con una lista simple de todos los joruneys.

---

### 3. `compile-storefront-use-cases`
* **Objetivo:** Unificar en un solo documento los últimos resultados de análisis generados por `analyze-journey-use-cases`.
* **Input:** Descubrimiento automático de los últimos análisis (*no requiere input manual*).
* **Output:** Documento Markdown con todas las tablas de los casos de uso.

---

### 4. `create-job`
* **Objetivo:** Generar o refactorizar archivos de definición de jobs (`JOB.md`) bajo la plantilla canónica RFC.
* **Input:** Descripción de requerimientos o borrador/archivo legado de job.
* **Output:** Archivo de código en repositorio (*Project Output*) ubicado en [`JOB.md`](file:///home/user/projects/graph-engineering-lite-skill/graph-engineering/jobs/create-job/JOB.md).

---

### 5. `define-journey-use-case-dtos`
* **Objetivo:** Definir DTOs de respuesta backend e ilustrar el flujo de datos entre Storefront, paquetes, Medusa y Supabase.
* **Input:** Un *journey* (kebab-case), casos de uso (camelCase) y opcionalmente contexto previo del diagrama Mermaid.
* **Output:** Archivo TypeScript en `apis/[journey]/domain/contracts/[journey].contract.ts` (*Project Output*) y diagrama Mermaid en Markdown 

---

### 6. `scaffold-journey-architecture`
* **Objetivo:** Generar la estructura base de carpetas y archivos (Domain, Application, Infrastructure) para uno o más *journeys*.
* **Input:** Uno o varios identificadores de *journey* (kebab-case).
* **Output:** Archivos de código (*Project Output*) creados en `apps/storefront/apis/[journey]/...`.
