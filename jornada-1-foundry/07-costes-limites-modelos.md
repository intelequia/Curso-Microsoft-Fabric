# J1-M7 · Costes, límites, regiones y elección de modelo

**Duración:** 20 min · **Formato:** explicación + checklist

## Objetivos

1. Traducir decisiones técnicas a coste y riesgo operativo.
2. Conocer límites frecuentes: cuotas, TPM/RPM, región, herramientas y previews.
3. Crear un checklist de paso a producción.

## Contenido

El coste de una solución Foundry incluye más que el modelo:

- Tokens de entrada y salida.
- Embeddings e indexación.
- Azure AI Search.
- Storage y bases de datos.
- Evaluaciones y red teaming.
- Application Insights / Log Analytics.
- Tráfico de red y private endpoints.
- Coste de operación y revisión humana.

### Checklist de selección

| Pregunta | Decisión |
| --- | --- |
| ¿Qué calidad mínima necesito? | Modelo grande o razonador. |
| ¿Qué latencia máxima acepto? | Modelo mini, streaming o cache. |
| ¿Cuánto contexto uso? | Chunking, resumen, retrieval selectivo. |
| ¿Dónde deben procesarse los datos? | Región, DataZone, red privada. |
| ¿Qué herramientas necesita? | Compatibilidad de modelo y región. |
| ¿Cómo evito sobrecoste? | Límites, cuotas, logging y sampling. |

## Mensajes clave

- Un piloto sin límites de consumo no es un piloto controlado.
- La región condiciona modelos, herramientas y cumplimiento.
- La optimización empieza por medir tokens, latencia, errores y calidad.
