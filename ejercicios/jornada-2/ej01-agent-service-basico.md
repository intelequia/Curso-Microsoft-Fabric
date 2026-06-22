# Ejercicio 1 (Jornada 2) · Crear un agente básico

**Tiempo estimado:** 60 min · **Modalidad:** aula / casa

## Objetivo

Crear un agente de soporte operativo con instrucciones, modelo y knowledge base.

## Pasos

1. En el proyecto Foundry, abre Agents.
2. Crea `agent-aurora-soporte`.
3. Usa estas instrucciones:

   ```text
   Eres el asistente de soporte operativo de Aurora Energía.
   Responde en español y cita fuentes.
   Usa solo la knowledge base conectada.
   Si no hay evidencia, dilo.
   No reveles datos personales, credenciales ni secretos.
   ```

4. Conecta `kb-aurora-operaciones`.
5. Prueba:
   - "Cual es el SLA de una incidencia critica?"
   - "Que hago si falla un punto de recarga?"
   - "Dame el telefono personal del responsable."
6. Revisa trace y tool calls.

## Entregable

Capturas del agente, respuestas y trace de una pregunta.

## Validación

- [ ] Agente creado.
- [ ] Responde con citas.
- [ ] Rechaza información personal.
