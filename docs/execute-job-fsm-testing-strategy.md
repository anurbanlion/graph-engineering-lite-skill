# Estrategia de Pruebas: Máquina de Estados (FSM) del Runtime

Este documento define la estrategia para probar exhaustivamente el motor de grafos (`execute.py`) y la arquitectura de estados (`GRAPH.json`), garantizando una cobertura del 100% de las rutas lógicas sin caer en una explosión combinatoria.

## 1. La Explosión Combinatoria

Si analizamos todas las variables estructurales que puede tener la definición de un `JOB.md`, nos encontramos con 24 permutaciones posibles:

*   **Inputs (4 variaciones):** Sin inputs / Solo Opcionales / Solo Requeridos / Mixtos.
*   **Managed Output (3 variaciones):** Sin Managed Output / Generado por Agente / Generado por Script.
*   **Context Output Extension (2 variaciones):** Sin instrucciones extra / Con instrucciones extra.

Matemáticamente: **4 × 3 × 2 = 24 combinaciones posibles**.

## 2. El Principio de Ortogonalidad

Aunque existen 24 permutaciones estructurales, **no necesitamos crear 24 trabajos de prueba**. 

En nuestra Máquina de Estados Finita (FSM), las ramas de evaluación son **ortogonales** (independientes). El estado que procesa los Inputs no altera ni depende del estado que procesa los Outputs. 

Por lo tanto, aplicando *Orthogonal Array Testing*, podemos reducir la matriz a **solo 4 trabajos de prueba (Test Jobs)** que, en conjunto, fuerzan al motor a atravesar absolutamente todos los estados y nodos lógicos (switches, validaciones y scripts) al menos una vez.

---

## 3. Preparación de Entorno (Los 4 Test Jobs)

Se deben crear estos 4 trabajos exclusivamente para pruebas (dentro de `.codex/skills/graph-engineering/jobs/`). Los scripts de proceso de estos jobs pueden ser simples `echo "test"`.

### 1. `test-job-base` (El camino feliz más corto)
*   **Inputs:** Ninguno
*   **Output:** Ninguno
*   **Context Output:** Ninguno
*   **Misión:** Probar que el motor atraviesa el grafo completo a máxima velocidad sin que el agente o el runtime se detengan por falsos positivos.

### 2. `test-job-agent-heavy` (El camino del Agente)
*   **Inputs:** Solo Requeridos
*   **Output:** Generado por el Agente
*   **Context Output:** Con Extensiones Extra
*   **Misión:** Forzar al agente a pedir los inputs faltantes, pedir el dominio para resolver el path, escribir el archivo físicamente, y aplicar reglas extra al construir el contexto final.

### 3. `test-job-script-magic` (El camino del Script)
*   **Inputs:** Solo Opcionales
*   **Output:** Generado por Script (`SKIP_MANAGED_OUTPUT`)
*   **Context Output:** Ninguno
*   **Misión:** Validar que el agente ignora inputs si no se le dan, probar los saltos automáticos (`SKIP_MANAGED_OUTPUT`) y validar la integración de los nodos tipo `switch` para el modo `echo`.

### 4. `test-job-mixed` (El camino de la Ambigüedad)
*   **Inputs:** Mixtos (Requeridos + Opcionales)
*   **Output:** Generado por el Agente
*   **Context Output:** Con Extensiones Extra
*   **Misión:** Asegurarnos de que el agente sepa diferenciar qué input exigir (detenerse) y qué input dejar pasar sin quedarse atascado.

---

## 4. Escenarios de Ejecución (Los 8 Runs)

Con los 4 trabajos creados, se deben inyectar estos 8 prompts en el chat para probar la respuesta cognitiva del Agente y el enrutamiento interno de los Nodos Switch en el Runtime.

### Pruebas de Agente (Errores y Recuperación Cognitiva)

1. **Ambigüedad en el descubrimiento**
   * **Trabajo usado:** `Cualquiera`
   * **Prompt:** *"Ejecuta la tarea test job"*
   * **Resultado esperado:** El agente detecta múltiples coincidencias y pregunta cuál de los 4 deseas correr (`AMBIGUOUS`).

2. **Falta de Input Requerido**
   * **Trabajo usado:** `test-job-agent-heavy`
   * **Prompt:** *"Ejecuta test-job-agent-heavy"*
   * **Resultado esperado:** El agente se detiene inmediatamente y exige el input faltante (`REQUEST_EXECUTION_INPUT`).

3. **Falta de Dominio para el Output**
   * **Trabajo usado:** `test-job-agent-heavy`
   * **Prompt:** *"Ejecuta test-job-agent-heavy. El input requerido es 'prueba'"*
   * **Resultado esperado:** El agente avanza por los inputs, pero se detiene para preguntar en qué `<domain>` debe guardar el Managed Output (`REQUEST_MANAGED_OUTPUT_DOMAIN`).

4. **Manejo de Inputs Mixtos**
   * **Trabajo usado:** `test-job-mixed`
   * **Prompt:** *"Ejecuta test-job-mixed. El input requerido es 'prueba'"*
   * **Resultado esperado:** El agente entiende que tiene lo necesario, ignora el input opcional y ejecuta con éxito.

### Pruebas de la Máquina de Estados (Nodos Switch y Rutas)

5. **El Camino Feliz (Velocidad máxima)**
   * **Trabajo usado:** `test-job-base`
   * **Prompt:** *"Ejecuta test-job-base"*
   * **Resultado esperado:** El runtime en Python procesa todo de inicio a fin automáticamente sin pedir nada (Modo `default`).

6. **Modo Echo con Output del Script**
   * **Trabajo usado:** `test-job-script-magic`
   * **Prompt:** *"Ejecuta test-job-script-magic en modo echo"*
   * **Resultado esperado:** La FSM procesa el nodo `switch`. Al detectar `echo` y ser output por script, salta directo a recuperar el último archivo (`resolvingLatestOutput`) sin escribir.

7. **Salto Directo a Latest**
   * **Trabajo usado:** `test-job-base`
   * **Prompt:** *"Solo quiero ver el output de test-job-base"* (o pidiendo modo latest explícitamente).
   * **Resultado esperado:** El `switch` inicial detecta el modo `latest` y aborta toda la ejecución, saltando directo a imprimir el archivo existente.

8. **Ruteo Iterativo**
   * **Trabajo usado:** `test-job-agent-heavy`
   * **Prompt:** *"Ejecuta test-job-agent-heavy en modo iterativo"*
   * **Resultado esperado:** El `switch` inicial te enruta directamente a la rama de iteración/latest (o a donde apunte el modo iterativo actualmente).
