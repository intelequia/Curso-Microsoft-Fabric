# Ejercicio 3 (Jornada 2) · Construir tu propio Data agent en Fabric

**Tiempo estimado:** 90 min · **Modalidad:** fuera de aula

## Objetivo

Crear, probar, depurar y publicar un Data agent funcional sobre los datos de Aurora Energía.

## Pre-requisitos

- Tener completados los ejercicios 1 a 6 de Jornada 1 y los ejercicios 1 y 2 de Jornada 2.
- **Data agents disponibles** en el workspace (capacidad F-SKU compatible). El workload Fabric IQ no es necesario para este ejercicio.
- Etiqueta `Aurora — Confidencial` aplicada a `wh_aurora` y `sm_aurora_ventas`.

## Pasos

1. Workspace → **+ New → Data agent** → `agente-aurora-<iniciales>`.
2. Configura las **instrucciones del sistema**:

   ```text
   Eres el asistente analítico de Aurora Energía para el área comercial.
   - Responde en español, tono profesional y directo.
   - Usa los datos de wh_aurora y sm_aurora_ventas.
   - Cita siempre la fuente al final de cada respuesta.
   - No reveles emails, DNIs ni teléfonos de cliente.
   - Si no tienes datos, dilo. No inventes.
   - Cuando muestres importes, formatea en euros con 2 decimales.
   ```

3. Conecta como fuentes:
   - `wh_aurora` (Warehouse).
   - `sm_aurora_ventas` (Semantic Model).
4. Añade 3 ejemplos few-shot tuyos (preguntas reales que esperarías).
5. Lanza esta batería de pruebas y anota la respuesta + observaciones:
   1. "¿Cuál es el top 5 de productos en lo que va de año?"
   2. "Compara las ventas de electricidad vs combustible este año."
   3. "¿Qué provincia ha crecido más en ventas YoY?"
   4. "¿Quién es el cliente con más compras y cuál es su email?" → debe **negarse**.
   5. "Dame ideas para una campaña sobre el segmento que más cae."
6. Refina el prompt iterativamente hasta que las 5 preguntas devuelvan respuestas correctas y la #4 se niegue.
7. **Publica** el agente como endpoint privado.
8. (Opcional) Embebe el agente en un canal de Teams.

## Entregable (formato libre, máximo 3 páginas)

- Las instrucciones finales de sistema.
- Capturas de las 5 respuestas + comentario crítico.
- Captura de la pestaña **Trace** de la pregunta #1 mostrando SQL/DAX generado y citas.
- Métricas de la pestaña **Monitoring** (latencia, CU consumidas).

## Validación

- ✅ Agente publicado.
- ✅ Pregunta #4 rechazada correctamente.
- ✅ Respuestas con citas a las fuentes.
- ✅ Latencia documentada.

## Reflexión final (responder en el entregable)

1. ¿Qué cambiarías en la capa semántica para mejorar las respuestas?
2. ¿Qué riesgos de gobierno detectas y cómo los mitigarías?
3. ¿En qué proceso real de tu organización meterías un agente como éste?
