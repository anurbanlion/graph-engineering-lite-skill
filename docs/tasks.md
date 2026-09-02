# Roadmap de Graph Engineering

## Hito 1: Migrar Graph Engineering a la carpeta local

- [ ] Migrar la implementación actual de `graph-engineering/` a `.graph-engineering/local/`.
  - [x] Analizar el contenido actual de `graph-engineering/` y `.graph-engineering/local/`.
  - [x] Respaldar íntegramente `.graph-engineering/local/` antes de reemplazar su contenido.
  - [x] Copiar todo el contenido de `graph-engineering/` a `.graph-engineering/local/`.
  - [x] Comparar el respaldo con la nueva carpeta local archivo por archivo.
  - [x] Recuperar `jobs/design-job-v2/JOB.md` desde el respaldo local.
  - [x] Recuperar `jobs/design-job-v2/GRAPH.json` desde el respaldo local.
  - [x] Recuperar `jobs/design-job-v2/GRAPH.md` desde el respaldo local.
  - [x] Recuperar `scripts/graph_to_mermaid.py` desde el respaldo local.
  - [x] Recuperar `scripts/resolve_local_job_path.py` desde el respaldo local.
  - [ ] Elimnar directorios `__pycache__/` en local si alguno llegó a copiarse.
  - [ ] Validar que los jobs, graphs, scripts, templates y documentos estén completos en `.graph-engineering/local/`.
  - [ ] Revisar el diff completo de la migración antes de cerrar el hito.
  - [ ] Crear un commit que registre exclusivamente la migración completa a `.graph-engineering/local/`.

## Hito 2: Migrar y redirigir la sincronización

- [x] Migrar el sincronizador de MJS a Python.
  - [x] Analizar `bin/sync-folder.mjs`, `bin/sync-folder.sh`, `bin/sync-folder.bat` y el contrato actual de `.env`.
  - [x] Crear una implementación Python que reproduzca uno a uno el comportamiento de `bin/sync-folder.mjs`.
    - [x] Leer `SYNC_SOURCE_PATH` y `SYNC_DESTINATION_PATH` desde `.env` con el mismo contrato actual.
    - [x] Interpretar fuentes simples, fuentes múltiples, destinos múltiples y `destinationName` de la misma forma.
    - [x] Resolver las rutas relativas desde la raíz del repositorio y exigir destinos absolutos.
    - [x] Aplicar las mismas validaciones de existencia, tipo y solapamiento de rutas.
    - [x] Crear las raíces de destino requeridas antes de sincronizar.
    - [x] Reemplazar completamente cada destino antes de copiar su fuente correspondiente.
    - [x] Conservar timestamps y reportar las fuentes y los destinos sincronizados.
  - [x] Actualizar `bin/sync-folder.sh` y `bin/sync-folder.bat` para delegar al sincronizador Python.

- [x] Redirigir la sincronización a `.graph-engineering/local/` como fuente de verdad global.
  - [x] Configurar `.env` con `{"path":".graph-engineering/local","destinationName":"graph-engineering"}` como fuente del skill.
  - [x] Configurar temporalmente en `.env` un destino controlado para la prueba.
  - [x] Ejecutar un run de prueba de la sincronización.
  - [x] Verificar que el run distribuya el contenido local bajo el nombre `graph-engineering` sin alterar la fuente de verdad.
  - [x] Restaurar en `.env` los destinos de sincronización registrados actualmente en `.env.example`.
  - [x] Crear un commit que registre la migración a Python y la redirección de la sincronización.

## Hito 3: Crear Execute Script para el agente

- [x] Crear `.graph-engineering/local/scripts/execute_script.py` como una utilidad invocable directamente por el agente.
  - [x] Aceptar un identificador de script, el Project Root y argumentos opcionales para el script resuelto.
  - [x] Resolver el identificador mediante el resolvedor de scripts existente en `.graph-engineering/local/scripts/`.
  - [x] Ejecutar únicamente scripts Python durante la primera versión.

- [x] Actualizar `.graph-engineering/local/SKILL.md` para utilizar Execute Script.
  - [x] Indicar que el agente debe invocarlo solamente ante la instrucción explícita `Execute the script <script-identifier>.` en un proceso normal o runtime state.
  - [x] Explicar cómo proporcionar el Project Root, el identificador y los argumentos del script.
  - [x] Añadir ejemplos de instrucciones con y sin argumentos y su interpretación por el skill.
  - [x] Aclarar que la primera versión admite solamente archivos `.py`.


## Hito 4: Incorporar el nodo especial `spawn`

- [x] Diseñar el contrato del nodo `spawn`.
  - [x] Diferenciar `spawn` de los nodos de instrucciones, decisión y script.
  - [x] Redefinir el grafo de execute
  - [x] Redefinir el modelo de datos de execute
  - [x] Diseñar el comportamiento de `spawn` dentro del grafo mermaid
  - [x] Planificar las tareas de implementación
  - [x] Implementar el nodo `spawn` y otras mejoras en el runtime.

- [x] Actualizar `execute-job` para usar `context.job_name` desde el inicio de la ejecución.
  - [x] Leer `context.job_name` cuando se proporcione al iniciar el runtime.
  - [x] Omitir el discovery del job cuando el contexto ya contenga un identificador de job válido.
  - [x] Conservar el discovery actual cuando `context.job_name` no esté disponible.
  - [x] Actualizar el grafo

- [x] Actualizar `execute-job` para usar `spawn` node para invocar a los otros jobs si tienen un GRAPH asociado.
- [x] Formalizar las actualizaciones de contexto declaradas por las transiciones.
  - [x] Incorporar `context_updates` como metadatos estructurados del contrato de transición.
  - [x] Validar las claves declaradas contra `context_schema`.
  - [x] Mostrar las actualizaciones de contexto en los diagramas Mermaid sin depender de instrucciones en lenguaje natural.
  - [x] Actualizar el runtime y el skill para interpretar las actualizaciones estructuradas.

- [x] Migrar todos los cambios a la carpeta de skills
- [ ] Crear un job con design-job-v2: `generate-job-diagram`
- [ ] Eliminar `execute-flow` ya que `execute-job` se volverá el orquestador oficial al poder invocar otros jobs.

## Hito 5: Completar `design-job-v2`

- [ ] Finalizar el diseño nodo por nodo de `design-job-v2`.
  - [ ] Revisar las instrucciones de cada estado y cada transición con el usuario.
  - [ ] Mantener `interviewing` como una entrevista continua de propósito, inputs, outputs y proceso.
  - [ ] Resolver el identificador y el path relativo agrupado antes de resolver la carpeta local.
  - [ ] Resolver la carpeta del job mediante el identificador del script local correspondiente.
  - [ ] Mantener el diseño y la revisión iterativa del graph cuando el proceso requiera un graph.
  - [ ] Escribir `JOB.md` tanto para jobs basados en pasos como para jobs basados en `GRAPH.json`.
  - [ ] Diseñar el pseudocódigo y el plan de reutilización antes de implementar scripts locales.
  - [ ] Completar directamente cuando el job no requiera scripts.
- [ ] Consolidar los artefactos producidos por `design-job-v2`.
  - [ ] Tratar `JOB.md`, `GRAPH.json`, `GRAPH.md` y `scripts/` como Project Outputs.
  - [ ] Evitar declarar un Managed Output para la materialización local del job.
  - [ ] Ejecutar el generador de Mermaid después de cada modificación de `GRAPH.json`.
  - [ ] Mantener el generador de Mermaid disponible como script local identificado.
  - [ ] Validar que todos los artefactos permanezcan dentro de la carpeta local resuelta para el job.
- [ ] Reemplazar el `design-job` actual con `design-job-v2`.
  - [ ] Renombrar la carpeta y el identificador de `design-job-v2` a `design-job`.
  - [ ] Actualizar las referencias que todavía utilicen el identificador temporal `design-job-v2`.
  - [ ] Sustituir los artefactos del `design-job` anterior únicamente después de validar la nueva implementación.
  - [ ] Eliminar el nombre temporal `design-job-v2` cuando la sustitución esté completa.

## Hito 5.1: Mejorar el diseño de grafos en `design-job-v2`

- [ ] Incorporar referencias y ejemplos de `GRAPH.json` al flujo de `design-job-v2`.
  - [ ] Documentar el esquema mínimo de un grafo: `id`, `version`, `context_schema`, `context`, `initial` y `states`.
  - [ ] Documentar los tipos de estado (`instruction`, `script`, `spawn` y `final`) y sus contratos.
  - [ ] Añadir un ejemplo anotado de estados, transiciones, condiciones, códigos de salida y actualizaciones de contexto.
  - [ ] Hacer que el agente consulte esas referencias durante la conversación de diseño antes de proponer el `GRAPH.json`.
  - [ ] Validar el grafo generado con el esquema y regenerar `GRAPH.md` como parte de la revisión.

## Hito 5.2: Probar la integración y el intercambio de contexto entre jobs

- [ ] Diseñar y validar un grafo mínimo que comparta `context.job_name` entre estados y jobs hijo.
  - [ ] Definir el contrato para propagar contexto desde un job padre a un job hijo.
  - [ ] Probar la validación del `job_name` mediante `check_graph` y `resolve_local_job_path`.
  - [ ] Documentar las limitaciones actuales de integración, especialmente la propagación y actualización de contexto.
  - [ ] Registrar los resultados de las pruebas y los cambios necesarios en el runtime o en el skill.

## Hito 5.3: Tratar `complete` y `abort` como estados implícitos del runtime

- [ ] Actualizar el contrato de graphs para que `complete` y `abort` no deban declararse en `states`.
  - [ ] Ajustar la validación de `execute.py` para aceptar transiciones hacia esos estados reservados.
  - [ ] Ajustar `graph_to_mermaid.py` para renderizar los estados reservados sin exigir definiciones locales.
  - [ ] Definir el comportamiento de entrada a `complete` y `abort` y sus resultados (`DONE` y `ERROR`).
  - [ ] Añadir pruebas de ejecución y generación Mermaid para ambos estados implícitos.


## Hito 6: Crear update job
- [ ] Diseñar `update-job` para modificar jobs locales existentes.
  - [ ] Definir su propósito, sus inputs, sus Project Outputs y su Context Output.
  - [ ] Resolver el job objetivo mediante su identificador y su Project Root.
  - [ ] Inspeccionar `JOB.md`, `GRAPH.json`, `GRAPH.md` y los scripts existentes antes de proponer cambios.
  - [ ] Preservar cambios locales ajenos al alcance de la actualización.
  - [ ] Regenerar `GRAPH.md` cuando cambie `GRAPH.json`.
  - [ ] Validar los artefactos actualizados antes de completar la ejecución.
- [ ] Implementar `update-job` dentro de `.graph-engineering/local/jobs/`.
  - [ ] Crear su `JOB.md`.
  - [ ] Crear su `GRAPH.json` cuando el proceso acordado justifique una máquina de estados.
  - [ ] Crear solamente los scripts locales requeridos por el diseño aprobado.
  - [ ] Documentar un ejemplo realista de actualización de un job local.

## Hito 6: Crear commit job?

## Hito 7: Formalizar el desarrollo y la calidad de scripts

- [ ] Crear un skill para elaborar especificaciones.
  - [ ] Guiar la definición del comportamiento esperado antes de implementar código.
  - [ ] Separar requisitos funcionales, restricciones, casos límite y criterios de aceptación.
  - [ ] Producir especificaciones que puedan convertirse directamente en casos de prueba.
  - [ ] Integrar el skill con el diseño de scripts de Graph Engineering.
- [ ] Crear un skill para elaborar diagramas de flujo.
  - [ ] Guiar la traducción de procesos y pseudocódigo a diagramas verificables.
  - [ ] Representar decisiones, bucles, errores, entradas y salidas de forma explícita.
  - [ ] Integrar el skill con el generador de Mermaid disponible en el proyecto.
  - [ ] Utilizar los diagramas como revisión previa a la implementación.
- [ ] Establecer un flujo verificable para desarrollar scripts.
  - [ ] Especificar el comportamiento antes de escribir el script.
  - [ ] Diagramar el flujo cuando existan decisiones, bucles o varias rutas de error.
  - [ ] Diseñar el pseudocódigo y revisar oportunidades de reutilización.
  - [ ] Implementar el script a partir de la especificación aprobada.
  - [ ] Crear pruebas derivadas de los criterios de aceptación.
  - [ ] Ejecutar las pruebas y registrar las validaciones antes de considerar completo el script.
- [ ] Aplicar `INSTRUCTION_AUTHORING.md` a las instrucciones del skill que requieren ejecutar scripts.
  - [ ] Revisar las instrucciones y reglas de `execute_script` para que cumplan la convención de authoring.
  - [ ] Añadir o ajustar ejemplos de instrucciones de scripts y de la interpretación correspondiente por el agente.

- [ ] Aplicar el flujo de calidad a los scripts críticos existentes.
  - [ ] Priorizar el executor, los resolvedores, el sincronizador y el generador de diagramas.
  - [ ] Añadir especificaciones y pruebas donde actualmente solo exista implementación.
  - [ ] Corregir divergencias entre comportamiento, documentación y graphs consumidores.

## Hito 8: Migrar las librerías CommonJS/MJS a Python

- [ ] Migrar `lib/resolve-paths.mjs` a Python.
  - [ ] Buscar las referencias a `lib/resolve-paths.mjs`.
  - [ ] Reimplementar su comportamiento en Python.
  - [ ] Reemplazar las referencias por la implementación Python o su identificador.
  - [ ] Validar la implementación y regenerar `GRAPH.md` cuando cambie un `GRAPH.json` consumidor.
- [ ] Migrar `lib/activity-logs.mjs` a Python.
  - [ ] Buscar las referencias a `lib/activity-logs.mjs`.
  - [ ] Reimplementar su comportamiento en Python.
  - [ ] Reemplazar las referencias por la implementación Python o su identificador.
  - [ ] Validar la implementación y regenerar `GRAPH.md` cuando cambie un `GRAPH.json` consumidor.
- [ ] Migrar `lib/graphs.mjs` a Python.
  - [ ] Buscar las referencias a `lib/graphs.mjs`.
  - [ ] Reimplementar su comportamiento en Python.
  - [ ] Reemplazar las referencias por la implementación Python o su identificador.
  - [ ] Validar la implementación y regenerar `GRAPH.md` cuando cambie un `GRAPH.json` consumidor.
- [ ] Migrar `lib/jobs.mjs` a Python.
  - [ ] Buscar las referencias a `lib/jobs.mjs`.
  - [ ] Reimplementar su comportamiento en Python.
  - [ ] Reemplazar las referencias por la implementación Python o su identificador.
  - [ ] Validar la implementación y regenerar `GRAPH.md` cuando cambie un `GRAPH.json` consumidor.
- [ ] Migrar `resolve-output-path.mjs` a Python.
  - [ ] Buscar las referencias a `resolve-output-path.mjs`.
  - [ ] Reimplementar su comportamiento en Python.
  - [ ] Reemplazar las referencias por la implementación Python o su identificador.
  - [ ] Validar la implementación y regenerar `GRAPH.md` cuando cambie un `GRAPH.json` consumidor.
- [ ] Migrar `read-job-template.mjs` a Python.
  - [ ] Buscar las referencias a `read-job-template.mjs`.
  - [ ] Reimplementar su comportamiento en Python.
  - [ ] Reemplazar las referencias por la implementación Python o su identificador.
  - [ ] Validar la implementación y regenerar `GRAPH.md` cuando cambie un `GRAPH.json` consumidor.
- [ ] Migrar `read-jobs.mjs` a Python.
  - [ ] Buscar las referencias a `read-jobs.mjs`.
  - [ ] Reimplementar su comportamiento en Python.
  - [ ] Reemplazar las referencias por la implementación Python o su identificador.
  - [ ] Validar la implementación y regenerar `GRAPH.md` cuando cambie un `GRAPH.json` consumidor.
- [ ] Migrar `read-graphs.mjs` a Python.
  - [ ] Buscar las referencias a `read-graphs.mjs`.
  - [ ] Reimplementar su comportamiento en Python.
  - [ ] Reemplazar las referencias por la implementación Python o su identificador.
  - [ ] Validar la implementación y regenerar `GRAPH.md` cuando cambie un `GRAPH.json` consumidor.
- [ ] Migrar `list-jobs.mjs` a Python.
  - [ ] Buscar las referencias a `list-jobs.mjs`.
  - [ ] Reimplementar su comportamiento en Python.
  - [ ] Reemplazar las referencias por la implementación Python o su identificador.
  - [ ] Validar la implementación y regenerar `GRAPH.md` cuando cambie un `GRAPH.json` consumidor.
- [ ] Migrar `list-graphs.mjs` a Python.
  - [ ] Buscar las referencias a `list-graphs.mjs`.
  - [ ] Reimplementar su comportamiento en Python.
  - [ ] Reemplazar las referencias por la implementación Python o su identificador.
  - [ ] Validar la implementación y regenerar `GRAPH.md` cuando cambie un `GRAPH.json` consumidor.
- [ ] Migrar `validate-graph.mjs` a Python.
  - [ ] Buscar las referencias a `validate-graph.mjs`.
  - [ ] Reimplementar su comportamiento en Python.
  - [ ] Reemplazar las referencias por la implementación Python o su identificador.
  - [ ] Validar la implementación y regenerar `GRAPH.md` cuando cambie un `GRAPH.json` consumidor.
- [ ] Migrar `get-latest-output-by-job.mjs` a Python.
  - [ ] Buscar las referencias a `get-latest-output-by-job.mjs`.
  - [ ] Reimplementar su comportamiento en Python.
  - [ ] Reemplazar las referencias por la implementación Python o su identificador.
  - [ ] Validar la implementación y regenerar `GRAPH.md` cuando cambie un `GRAPH.json` consumidor.
- [ ] Migrar `dump-latest-output.mjs` a Python.
  - [ ] Buscar las referencias a `dump-latest-output.mjs`.
  - [ ] Reimplementar su comportamiento en Python.
  - [ ] Reemplazar las referencias por la implementación Python o su identificador.
  - [ ] Validar la implementación y regenerar `GRAPH.md` cuando cambie un `GRAPH.json` consumidor.
- [ ] Migrar `custom/compile-application-journeys.mjs` a Python.
  - [ ] Buscar las referencias a `custom/compile-application-journeys.mjs`.
  - [ ] Reimplementar su comportamiento en Python.
  - [ ] Reemplazar las referencias por la implementación Python o su identificador.
  - [ ] Validar la implementación y regenerar `GRAPH.md` cuando cambie un `GRAPH.json` consumidor.
- [ ] Migrar `custom/compile-application-use-cases.mjs` a Python.
  - [ ] Buscar las referencias a `custom/compile-application-use-cases.mjs`.
  - [ ] Reimplementar su comportamiento en Python.
  - [ ] Reemplazar las referencias por la implementación Python o su identificador.
  - [ ] Validar la implementación y regenerar `GRAPH.md` cuando cambie un `GRAPH.json` consumidor.
- [ ] Migrar `custom/compile-initiatives.mjs` a Python.
  - [ ] Buscar las referencias a `custom/compile-initiatives.mjs`.
  - [ ] Reimplementar su comportamiento en Python.
  - [ ] Reemplazar las referencias por la implementación Python o su identificador.
  - [ ] Validar la implementación y regenerar `GRAPH.md` cuando cambie un `GRAPH.json` consumidor.
- [ ] Migrar `custom/scaffold-journey-architecture.mjs` a Python.
  - [ ] Buscar las referencias a `custom/scaffold-journey-architecture.mjs`.
  - [ ] Reimplementar su comportamiento en Python.
  - [ ] Reemplazar las referencias por la implementación Python o su identificador.
  - [ ] Validar la implementación y regenerar `GRAPH.md` cuando cambie un `GRAPH.json` consumidor.
- [ ] Migrar `custom/scaffold-landing-page.mjs` a Python.
  - [ ] Buscar las referencias a `custom/scaffold-landing-page.mjs`.
  - [ ] Reimplementar su comportamiento en Python.
  - [ ] Reemplazar las referencias por la implementación Python o su identificador.
  - [ ] Validar la implementación y regenerar `GRAPH.md` cuando cambie un `GRAPH.json` consumidor.
- [ ] Migrar `custom/scan-open-communication-tasks.mjs` a Python.
  - [ ] Buscar las referencias a `custom/scan-open-communication-tasks.mjs`.
  - [ ] Reimplementar su comportamiento en Python.
  - [ ] Reemplazar las referencias por la implementación Python o su identificador.
  - [ ] Validar la implementación y regenerar `GRAPH.md` cuando cambie un `GRAPH.json` consumidor.
- [ ] Retirar cada implementación `.mjs` únicamente después de validar su reemplazo Python y todas sus referencias.

- [ ] Agregar en wsl patch la politica de un reintento

- wsl patch deberia tener soporte multi archivo, y ser un job ahora que lo pienso

## Contexto y dirección del proyecto

Este repositorio debe funcionar como la fuente principal de desarrollo de Graph Engineering, aunque su implementación canónica viva dentro de `.graph-engineering/local/`. A diferencia de un proyecto consumidor, que normalmente conservará allí solo jobs, graphs, scripts o personalizaciones puntuales, este repositorio mantendrá una copia completa y editable del skill. La estructura local permitirá desarrollar y ejecutar los mismos artefactos mediante el runtime real antes de sincronizarlos con los destinos de instalación o distribución.

La sincronización debe dejar de considerar `graph-engineering/` como la fuente principal. Su nueva responsabilidad será publicar o replicar el contenido canónico de `.graph-engineering/local/` hacia los destinos definidos, sin confundir archivos de desarrollo con artefactos generados ni destruir extensiones locales. La carpeta antigua deberá mantenerse únicamente durante la transición y eliminarse después de comprobar la equivalencia funcional de la nueva estructura.

La resolución por identificadores desacoplará los graphs de las ubicaciones físicas de los scripts. El executor de la primera etapa será deliberadamente pequeño y admitirá solo Python; por eso las referencias heredadas a `.mjs` deberán inventariarse y migrarse de forma controlada. El Project Root explícito será la base determinística para encontrar tanto los artefactos completos de este repositorio como las copias parciales de otros proyectos.

El nodo `spawn` será el mecanismo explícito para componer máquinas de estados y ejecutar jobs o graphs hijos. Esta responsabilidad no debe ocultarse dentro de los nodos de script ni resolverse mediante propagación implícita de submáquinas. Su contrato deberá hacer visibles la relación padre-hijo, el contexto transmitido y el resultado que reanuda a la máquina padre.

El hito de calidad busca corregir una carencia del flujo actual: los scripts suelen implementarse antes de que existan una especificación verificable, un flujo revisado y pruebas derivadas de criterios de aceptación. Los skills de creación de especificaciones y diagramas de flujo deberán convertir esas actividades en pasos reutilizables, de modo que diseñar, implementar, probar y validar scripts sea un proceso sistemático y no una decisión improvisada en cada job.
