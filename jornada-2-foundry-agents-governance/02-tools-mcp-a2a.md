# J2-M2 · Herramientas: web, code, file search, functions, MCP y A2A

**Duración:** 35 min · **Formato:** explicación + demo

## Objetivos

1. Conocer las herramientas disponibles para agentes.
2. Elegir entre herramientas integradas y herramientas custom.
3. Entender MCP, OpenAPI y A2A como patrones de integración.

## Contenido

Las herramientas permiten que un agente salga del texto: buscar, calcular, leer documentos, llamar APIs o coordinarse con otros agentes.

### Herramientas frecuentes

| Herramienta | Uso |
| --- | --- |
| Web search | Información actual con citas web. |
| Code Interpreter | Python sandbox para análisis y gráficos. |
| File Search | Retrieval sobre documentos subidos. |
| Function calling | Funciones ejecutadas por tu aplicación. |
| OpenAPI tool | Conectar APIs HTTP descritas por OpenAPI. |
| MCP | Exponer herramientas compartidas como servidor estándar. |
| A2A | Comunicación entre agentes compatibles. |
| Toolbox | Paquete versionado de herramientas reutilizable. |

## Criterio de elección

- Usa built-in tools para acelerar prototipos.
- Usa OpenAPI si ya existe una API gobernada.
- Usa MCP si varias aplicaciones o agentes compartirán herramientas.
- Usa function calling local para lógica simple controlada por la aplicación.
- Usa A2A solo cuando haya agentes con responsabilidad separada.

## Demo en vivo

1. Añadir File Search o knowledge base al agente.
2. Añadir una función simulada para consultar incidencias.
3. Preguntar "¿Hay incidencias críticas abiertas y qué procedimiento aplica?"
4. Ver en trace qué herramienta se invocó.

## Mensajes clave

- Una herramienta mal acotada convierte al agente en riesgo operativo.
- La autenticación de herramientas debe diseñarse antes de publicar.
- MCP y toolboxes ayudan a gobernar herramientas compartidas.
