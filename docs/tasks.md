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

## Hito 2: Redirigir la sincronización a la fuente local

- [ ] Redirigir la sincronización a `.graph-engineering/local/` como fuente de verdad global.
  - [ ] Revisar `bin/sync-folder.mjs`, `bin/sync-folder.sh` y `bin/sync-folder.bat`.
  - [ ] Modificar los scripts para que sincronicen desde `.graph-engineering/local/` hacia los demás repositorios.
  - [ ] Ejecutar un run de prueba de la sincronización.
  - [ ] Verificar que el run de prueba distribuya el contenido local esperado sin alterar la fuente de verdad.
  - [ ] Crear un commit que registre exclusivamente la redirección de la sincronización.

## Hito 3: Consolidar la ejecución local de scripts

- [ ] Crear un executor dedicado para scripts `execute_script`.
  - [ ] Aceptar un identificador de script en lugar de una ruta física.
  - [ ] Resolver el identificador mediante el resolvedor de scripts existente.
  - [ ] Recibir el Project Root de forma explícita para resolver scripts locales determinísticamente.
  - [ ] Ejecutar únicamente scripts Python durante la primera versión.
  - [ ] Propagar la salida estándar, los errores y el resultado de ejecución al runtime del graph.
  - [ ] Mantener transiciones genéricas `done` y `error` cuando no existan resultados adicionales que distinguir.

- [ ] Actualizar el skill de Graph Engineering para utilizar el executor (local).
  - [ ] Explicar cómo proporcionar el Project Root al iniciar una ejecución.
  - [ ] Explicar cómo ejecutar un script mediante su identificador.
  - [ ] Añadir ejemplos de scripts globales y scripts locales.
  - [ ] Aclarar que la primera versión admite solamente archivos `.py`.

- [ ] Migrar las referencias heredadas a scripts `.mjs`.
  - [ ] Inventariar las referencias directas a archivos `.mjs` en jobs, graphs y documentación.
  - [ ] Convertir o reemplazar los scripts necesarios por implementaciones Python compatibles con el executor.
  - [ ] Sustituir rutas y extensiones explícitas por identificadores de script.
  - [ ] Regenerar los diagramas de todos los `GRAPH.json` modificados.
  - [ ] Retirar las implementaciones `.mjs` solamente después de comprobar su equivalencia funcional.

## Hito 4: Completar `design-job-v2`

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

## Hito 5: Crear el job de actualización

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

## Hito 6: Incorporar el nodo especial `spawn`

- [ ] Diseñar el contrato del nodo `spawn`.
  - [ ] Diferenciar `spawn` de los nodos de instrucciones, decisión y script.
  - [ ] Definir cómo identifica el job o graph hijo que debe ejecutar.
  - [ ] Definir cómo recibe el Project Root y el contexto inicial de la ejecución hija.
  - [ ] Definir cómo relaciona la ejecución hija con la ejecución padre.
  - [ ] Definir cómo transforma la finalización o el error del hijo en transiciones del padre.
- [ ] Implementar el nodo `spawn` en el runtime.
  - [ ] Ampliar la validación del schema de graphs.
  - [ ] Crear el runtime hijo desde el executor principal.
  - [ ] Persistir la relación entre snapshots padre e hijo.
  - [ ] Reanudar la máquina padre con el Context Output de la máquina hija.
  - [ ] Propagar errores sin dejar ejecuciones parcialmente activas.
- [ ] Documentar el uso del nodo `spawn`.
  - [ ] Añadir un ejemplo mínimo de composición de jobs.
  - [ ] Añadir un ejemplo de submáquina con Project Root explícito.
  - [ ] Regenerar los diagramas de los graphs usados como ejemplo.

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
- [ ] Aplicar el flujo de calidad a los scripts críticos existentes.
  - [ ] Priorizar el executor, los resolvedores, el sincronizador y el generador de diagramas.
  - [ ] Añadir especificaciones y pruebas donde actualmente solo exista implementación.
  - [ ] Corregir divergencias entre comportamiento, documentación y graphs consumidores.

## Contexto y dirección del proyecto

Este repositorio debe funcionar como la fuente principal de desarrollo de Graph Engineering, aunque su implementación canónica viva dentro de `.graph-engineering/local/`. A diferencia de un proyecto consumidor, que normalmente conservará allí solo jobs, graphs, scripts o personalizaciones puntuales, este repositorio mantendrá una copia completa y editable del skill. La estructura local permitirá desarrollar y ejecutar los mismos artefactos mediante el runtime real antes de sincronizarlos con los destinos de instalación o distribución.

La sincronización debe dejar de considerar `graph-engineering/` como la fuente principal. Su nueva responsabilidad será publicar o replicar el contenido canónico de `.graph-engineering/local/` hacia los destinos definidos, sin confundir archivos de desarrollo con artefactos generados ni destruir extensiones locales. La carpeta antigua deberá mantenerse únicamente durante la transición y eliminarse después de comprobar la equivalencia funcional de la nueva estructura.

La resolución por identificadores desacoplará los graphs de las ubicaciones físicas de los scripts. El executor de la primera etapa será deliberadamente pequeño y admitirá solo Python; por eso las referencias heredadas a `.mjs` deberán inventariarse y migrarse de forma controlada. El Project Root explícito será la base determinística para encontrar tanto los artefactos completos de este repositorio como las copias parciales de otros proyectos.

El nodo `spawn` será el mecanismo explícito para componer máquinas de estados y ejecutar jobs o graphs hijos. Esta responsabilidad no debe ocultarse dentro de los nodos de script ni resolverse mediante propagación implícita de submáquinas. Su contrato deberá hacer visibles la relación padre-hijo, el contexto transmitido y el resultado que reanuda a la máquina padre.

El hito de calidad busca corregir una carencia del flujo actual: los scripts suelen implementarse antes de que existan una especificación verificable, un flujo revisado y pruebas derivadas de criterios de aceptación. Los skills de creación de especificaciones y diagramas de flujo deberán convertir esas actividades en pasos reutilizables, de modo que diseñar, implementar, probar y validar scripts sea un proceso sistemático y no una decisión improvisada en cada job.
