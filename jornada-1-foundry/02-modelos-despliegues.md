# J1-M2 · Model catalog, despliegues, endpoints y panorama ML

**Duración:** 35 min · **Formato:** explicación + demo

## Objetivos

1. Aprender a elegir modelos en el catálogo.
2. Entender opciones de despliegue, cuotas, regiones y límites.
3. Relacionar elección de modelo con coste, latencia, calidad y cumplimiento.
4. Ubicar la parte ML de Foundry sin entrar en entrenamiento ni MLOps.

## Contenido

Foundry centraliza el acceso a modelos de distintas familias. El catálogo permite comparar capacidades, proveedor, modalidad, región, licencia, benchmarks, disponibilidad de fine-tuning y tipo de endpoint.

### Familias habituales

| Familia | Uso típico |
| --- | --- |
| GPT-5 / GPT-4.1 | Razonamiento, asistencia general, tareas complejas y multimodalidad. |
| GPT-4.1 mini / nano | Latencia baja, alto volumen y coste controlado. |
| Claude | Razonamiento, código y tareas con contexto largo, según disponibilidad. |
| Mistral | Multilingüe, código y escenarios generalistas. |
| Phi | Modelos pequeños para casos eficientes o edge. |
| Llama / modelos abiertos | Personalización, control y escenarios open-weight. |

### Criterios de selección

- Calidad requerida y tolerancia al error.
- Latencia máxima aceptable.
- Volumen de tokens.
- Necesidad de multimodalidad.
- Región y residencia de datos.
- Compatibilidad con herramientas, agentes y evaluación.
- Coste por millón de tokens y coste de herramientas asociadas.

### Endpoints

| Endpoint | Uso |
| --- | --- |
| `services.ai.azure.com/api/projects/<project>` | Foundry SDK, Agent Service, herramientas y proyecto. |
| `openai.azure.com/openai/v1` | Compatibilidad OpenAI completa para modelos OpenAI desplegados. |
| Endpoints específicos de proveedor | Modelos de terceros cuando el proveedor requiere ruta propia. |

### La parte ML, solo como panorama

Foundry también cubre escenarios de **model builders**, no solo aplicaciones generativas. La conexión con ML aparece sobre todo en:

- Modelos abiertos o custom desplegados con **managed compute**.
- Uso de infraestructura y conceptos de Azure Machine Learning para hospedar modelos.
- Evaluación, fine-tuning o inferencia batch cuando el caso lo requiere.

En este curso no profundizamos en entrenamiento, jobs, pipelines, MLflow, registries ni MLOps. Eso pertenece a una formación específica de Azure Machine Learning. Aquí basta con que el alumno entienda que:

| Concepto | Qué diremos en clase |
| --- | --- |
| Managed compute | Despliegue de modelos sobre cómputo gestionado, con cuota de VM/SKU. |
| Custom/open models | Modelos fuera de los despliegues estándar/serverless. |
| Entrenamiento | Se cubre en la jornada de Azure Machine Learning Studio. |
| MLOps | Importante para equipos ML, no foco de esta formación Foundry. |

## Demo en vivo

1. Abrir Model catalog.
2. Filtrar por chat/completions y región.
3. Comparar un modelo capaz y uno mini.
4. Crear un deployment de laboratorio.
5. Mostrar nombre del deployment, endpoint y límites.
6. Mostrar, sin desplegar si no hay cuota, un modelo con opción de managed compute y explicar que es la puerta a escenarios ML.

## Mensajes clave

- El mejor modelo no siempre es el más grande.
- El coste real incluye tokens, herramientas, búsqueda, almacenamiento, evaluaciones y monitorización.
- Región y cuota son decisiones de arquitectura, no detalles administrativos.
- La parte ML existe, pero aquí se trata como contexto: el foco del curso son aplicaciones generativas, RAG y agentes.
