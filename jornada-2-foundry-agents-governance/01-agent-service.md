# J2-M1 · Foundry Agent Service y ciclo de vida

**Duración:** 35 min · **Formato:** explicación + demo

## Objetivos

1. Entender qué es un agente y qué aporta Agent Service.
2. Diferenciar prompt agents, hosted agents y agentes externos que llaman a Foundry.
3. Recorrer el ciclo create, test, trace, evaluate, publish y monitor.

## Contenido

Un agente combina modelo, instrucciones y herramientas para resolver tareas en varios pasos. Foundry Agent Service añade runtime gestionado, trazabilidad, publicación, versionado, identidad, seguridad y monitorización.

### Tipos

| Tipo | Uso |
| --- | --- |
| **Prompt agent** | Se define en portal/SDK y Foundry lo ejecuta sin mantener código de app. |
| **Hosted agent** | Código propio con Agent Framework, LangGraph u otros frameworks, alojado por Foundry. |
| **External agent** | Código fuera de Foundry que llama a Responses API y herramientas Foundry. |

### Ciclo de vida

1. Crear instrucciones y seleccionar modelo.
2. Añadir herramientas.
3. Probar en playground.
4. Revisar trazas y tool calls.
5. Evaluar con dataset.
6. Publicar como endpoint estable.
7. Monitorizar uso, errores, calidad y coste.

## Demo en vivo

1. Crear `agent-aurora-soporte`.
2. Añadir instrucciones de rol y restricciones.
3. Probar una pregunta simple.
4. Revisar la traza de ejecución.
5. Mostrar versionado/publicación.

## Mensajes clave

- Un agente no es un chatbot: decide cuándo usar herramientas.
- El valor empresarial aparece cuando hay herramientas, permisos y evaluación.
- Publicar sin trazas ni evaluación deja el riesgo invisible.
