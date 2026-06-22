# J1-M4 · Prompting, grounding y patrones RAG

**Duración:** 35 min · **Formato:** explicación + demo

## Objetivos

1. Diseñar instrucciones claras para aplicaciones empresariales.
2. Entender por qué el grounding reduce alucinaciones.
3. Reconocer patrones RAG simples, avanzados y agentic retrieval.

## Contenido

Un prompt empresarial no es una frase creativa: es una especificación operativa. Debe fijar rol, objetivo, fuentes permitidas, límites, formato, idioma, tratamiento de incertidumbre y políticas de seguridad.

### Patrón de instrucciones

```text
Eres el asistente de operaciones de Aurora Energía.
Responde en español, con tono profesional y directo.
Usa solo las fuentes conectadas al proyecto.
Si no hay evidencia suficiente, di que no tienes datos.
Cita documentos o registros usados.
No reveles datos personales ni secretos internos.
```

### Grounding

Grounding significa dar al modelo información recuperada en tiempo de ejecución:

- Documentos internos.
- Índices de Azure AI Search.
- Ficheros subidos al proyecto.
- Datos de negocio o APIs.
- Resultados de herramientas.

### Patrones RAG

| Patrón | Cuándo usarlo |
| --- | --- |
| RAG simple | FAQs, documentación estable y bajo riesgo. |
| RAG con metadatos | Documentos por área, país, versión o permiso. |
| RAG evaluado | Cuando necesitas medir groundedness y regresiones. |
| Agentic retrieval | Cuando el agente necesita planificar búsquedas o combinar fuentes. |

## Demo en vivo

1. Preguntar al modelo sin contexto.
2. Añadir contexto manual de un documento Aurora.
3. Comparar respuesta y citar evidencia.
4. Mostrar qué falla cuando el prompt permite inventar.

## Mensajes clave

- Prompting no sustituye datos correctos ni permisos.
- RAG aporta evidencia, pero debe evaluarse.
- La instrucción "si no sabes, dilo" debe probarse con preguntas trampa.
