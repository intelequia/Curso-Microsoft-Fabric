# Ejercicio 2 (Jornada 2) · Añadir herramienta de incidencias

**Tiempo estimado:** 75 min · **Modalidad:** casa

## Objetivo

Conectar una herramienta simulada para que el agente consulte incidencias abiertas.

## Pasos

1. Revisa `assets/data/incidencias.json`.
2. Ejecuta la herramienta local:

   ```bash
   python assets/code/mock_incidents_tool.py
   ```

3. Define una función o tool equivalente en Foundry, OpenAPI o function calling, según disponibilidad del tenant.
4. Actualiza instrucciones del agente:

   ```text
   Para preguntas sobre incidencias abiertas, usa la herramienta de incidencias.
   No inventes incidencias.
   Muestra solo id, severidad, estado, resumen y equipo propietario.
   ```

5. Prueba:
   - "Que incidencias criticas hay abiertas?"
   - "Hay incidencias de pagos abiertas?"
   - "Cierra la incidencia INC-2026-001" debe rechazarse si la tool solo es lectura.

## Entregable

Captura de tool call y respuesta final del agente.

## Validación

- [ ] El agente llama a la herramienta.
- [ ] No inventa incidencias.
- [ ] No ejecuta acciones no permitidas.
