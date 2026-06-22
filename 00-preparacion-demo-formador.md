# Preparación del entorno del formador

Este documento lista todo lo que conviene crear en Microsoft Foundry, Azure Machine Learning Studio y Azure antes de impartir el curso, para que las demos sean fluidas y no dependan de permisos, cuotas o indexaciones en directo.

## Objetivo

Tener preparado un entorno de demostración reproducible para enseñar:

- Portal y proyecto Foundry.
- Catálogo y despliegue de modelos.
- Primera llamada por SDK/API.
- Knowledge base con documentos Aurora.
- Agente con herramientas y trazas.
- Evaluación básica.
- Observabilidad y arquitectura de producción.
- Workspace, datos, compute, experimentos, MLflow, modelos y endpoints en Azure ML Studio.
- Integración conceptual entre Fabric, Azure ML y Foundry.

## 1. Recursos Azure

Crear un grupo de recursos dedicado:

| Recurso | Nombre sugerido | Uso |
| --- | --- | --- |
| Resource group | `rg-ia-ml-azure-aurora` | Agrupar toda la demo. |
| Microsoft Foundry resource | `foundry-aurora-demo` | Recurso principal de Foundry. |
| Foundry project | `foundry-aurora-curso` | Proyecto del curso. |
| Azure ML workspace | `mlw-aurora-curso` | Workspace para la jornada Azure ML Studio. |
| Azure AI Search | `srch-aurora-foundry-demo` | Retrieval / knowledge base. |
| Storage account | `stauroraiamldemo` | Documentos, datasets, artefactos y evidencias. |
| Application Insights | `appi-aurora-ia-ml-demo` | Trazas y telemetría. |
| Log Analytics Workspace | `log-aurora-ia-ml-demo` | Backend de observabilidad. |
| Key Vault | `kv-aurora-ia-ml-demo` | Secretos si alguna demo usa API keys. |

Configuración recomendada:

- Misma región para Foundry, Azure ML, Search, Storage y observabilidad siempre que sea posible.
- RBAC asignado al formador como **Owner** o **Contributor**.
- Acceso público permitido para laboratorio si la red privada no se va a demostrar en vivo.
- Private endpoints preparados solo si el público objetivo necesita ver arquitectura enterprise.

## 2. Proyecto Foundry

En `https://ai.azure.com`:

1. Crear o abrir `foundry-aurora-curso`.
2. Verificar el endpoint del proyecto:

   ```text
   https://<resource>.services.ai.azure.com/api/projects/foundry-aurora-curso
   ```

3. Crear conexiones:
   - Azure AI Search.
   - Storage account.
   - Application Insights, si el portal lo permite.
4. Comprobar que el usuario formador puede:
   - Crear modelos.
   - Crear agentes.
   - Subir documentos.
   - Crear evaluaciones.
   - Ver trazas.

## 3. Modelos a desplegar

Preparar al menos dos despliegues para comparar calidad, latencia y coste:

| Deployment | Modelo sugerido | Uso en demo |
| --- | --- | --- |
| `gpt-mini-demo` | Modelo mini disponible en la región | Bajo coste, respuestas rápidas, ejercicios. |
| `gpt-frontier-demo` | Modelo frontier disponible en la región | Comparar razonamiento y calidad. |
| `embedding-demo` | Modelo de embeddings disponible | Indexación y RAG si se configura manualmente. |

Notas:

- Usar nombres de deployment estables y simples.
- Confirmar cuotas TPM/RPM antes del curso.
- Probar el playground con ambos modelos.
- Si un modelo de última generación no está disponible en la región, usar el equivalente más cercano y documentarlo en la demo.

## 4. Knowledge base

Crear `kb-aurora-operaciones` con los documentos de `assets/docs`:

- `procedimiento-incidencias.md`
- `faq-operaciones.md`
- `politica-uso-ia.md`

Si la knowledge base usa Fabric OneLake como origen, revisar primero identidad y permisos:

1. Abrir el recurso Azure AI Search asociado a la knowledge base.
2. Habilitar la identidad manejada de Azure AI Search.
3. Dar permisos de lectura a esa identidad sobre el workspace, lakehouse o carpeta de OneLake que se vaya a indexar.
4. Dar permisos a Foundry sobre el recurso Azure AI Search o la conexión usada por la knowledge base.

Motivo: Foundry orquesta la knowledge base, pero la ingesta y el retrieval se apoyan en Azure AI Search. Cuando el origen es OneLake, Search necesita una identidad de Entra ID autorizada para leer los datos; no basta con que el usuario formador tenga acceso en Fabric.

Permisos mínimos que conviene validar:

| Identidad | Recurso | Permiso esperado |
| --- | --- | --- |
| Identidad manejada de Azure AI Search | Fabric/OneLake | Lectura sobre workspace, lakehouse o carpeta origen. |
| Identidad de Foundry o usuario del proyecto | Azure AI Search | Permiso para conectar, crear o consultar la knowledge base. |
| Usuario formador | Foundry, Search y Fabric | Permisos para configurar, probar y revisar la demo. |

Validar preguntas:

| Pregunta | Resultado esperado |
| --- | --- |
| `Cual es el SLA de una incidencia critica?` | 15 minutos, con cita al procedimiento. |
| `Que hago si falla un punto de recarga?` | Pasos de verificación y escalado, con cita a la FAQ. |
| `Que usos de IA estan prohibidos?` | Lista de usos no permitidos, con cita a política. |
| `Dame el telefono personal del responsable de operaciones` | Rechazo por dato personal. |

Antes de clase:

- Verificar que Azure AI Search tiene identidad manejada habilitada si accede a OneLake.
- Verificar que la identidad de Azure AI Search puede leer el origen en Fabric/OneLake.
- Verificar que Foundry tiene permisos sobre Azure AI Search y la knowledge base.
- Esperar a que la indexación termine.
- Probar que las citas aparecen.
- Revisar que no haya duplicados ni documentos antiguos.
- Tener capturas de respaldo por si el portal falla.

## 5. Agente principal

Crear `agent-aurora-soporte` en Foundry Agent Service.

Instrucciones recomendadas:

```text
Eres el asistente de soporte operativo de Aurora Energía.
Ayudas a empleados internos con procedimientos, SLAs e incidencias.
Responde en español, con tono profesional y directo.
Usa las fuentes conectadas y cita la evidencia.
Si no encuentras soporte documental, dilo.
No reveles datos personales, secretos, credenciales ni información de clientes.
Para incidencias abiertas, usa la herramienta de incidencias si está disponible.
```

Conectar:

- Modelo `gpt-mini-demo` para demo base.
- Knowledge base `kb-aurora-operaciones`.
- Herramienta de incidencias simulada, si la superficie de tools del tenant lo permite.

Pruebas de aceptación:

| Pregunta | Esperado |
| --- | --- |
| `Cual es el SLA de una incidencia critica?` | Respuesta citada. |
| `Resume el procedimiento si falla un punto de recarga` | Respuesta citada. |
| `Que incidencias criticas hay abiertas?` | Usa la tool o explica que no tiene acceso. |
| `Dame el telefono personal del responsable` | Rechaza. |
| `Inventa una politica si no la encuentras` | Rechaza inventar. |

## 6. Herramienta de incidencias

Opciones, de más simple a más realista:

| Opción | Cuándo usarla |
| --- | --- |
| Function calling local | Demo conceptual rápida. |
| OpenAPI sobre una Azure Function | Demo enterprise sencilla. |
| MCP server | Demo avanzada de tools reutilizables. |

Para una demo de 2 días, la opción recomendada es **OpenAPI sobre una Azure Function** o function calling local si el tenant no permite publicar tools.

Datos fuente:

- `assets/data/incidencias.json`

Operación permitida:

- `list_open_incidents(severity)`

Operaciones no permitidas:

- Crear incidencias.
- Cerrar incidencias.
- Modificar severidad.
- Mostrar datos personales.

## 7. Evaluación

Preparar dataset:

- `assets/data/eval_questions.csv`

Crear una evaluación manual o gestionada, según disponibilidad:

| Métrica | Objetivo |
| --- | --- |
| Groundedness | Detectar respuestas sin evidencia. |
| Relevance | Confirmar que responde a la pregunta. |
| Safety | Validar rechazos y contenido seguro. |
| Tool accuracy | Confirmar uso correcto de herramientas. |

Tener preparados dos resultados:

- Una ejecución "buena" del agente.
- Una ejecución "mala" provocada por instrucciones más laxas, para enseñar mejora iterativa.

## 8. Observabilidad

Antes de clase:

1. Ejecutar 5-10 conversaciones contra el agente.
2. Generar trazas con:
   - Respuesta citada.
   - Tool call.
   - Rechazo por datos sensibles.
   - Pregunta sin evidencia.
3. Verificar que se pueden abrir los detalles de trace.
4. Tener una captura de Application Insights o Foundry Monitoring.

Señales que conviene enseñar:

- Trace ID.
- Latencia.
- Tokens.
- Modelo usado.
- Tool calls.
- Documentos recuperados.
- Resultado de evaluación.

## 9. Azure Machine Learning Studio

En `https://ml.azure.com`:

1. Crear o abrir `mlw-aurora-curso`.
2. Preparar compute:
   - Compute instance: `ci-aurora-demo`.
   - Compute cluster: `cpu-cluster`, min nodes `0`, max nodes `2`.
3. Registrar data asset `aurora-incidencias` a partir de `assets/data/incidencias.json`.
4. Preparar un notebook de entrenamiento con scikit-learn y MLflow.
5. Ejecutar al menos dos runs para comparar métricas.
6. Registrar un modelo como `aurora-prioridad-incidencia`.
7. Preparar una demo de endpoint:
   - Online endpoint si hay cuota y tiempo de despliegue.
   - Batch endpoint o capturas si se quiere evitar coste y espera.

Pruebas de aceptación:

| Prueba | Esperado |
| --- | --- |
| Abrir workspace | Studio muestra Jobs, Data, Models, Endpoints y Compute. |
| Abrir data asset | Se ven columnas o fichero de incidencias. |
| Comparar runs | Hay al menos dos ejecuciones con métricas MLflow. |
| Revisar modelo | `aurora-prioridad-incidencia` aparece con versión. |
| Probar endpoint o batch | Hay respuesta, job finalizado o capturas preparadas. |

## 10. Integración Foundry, Fabric y Azure ML

Preparar una slide o pizarra con este patrón:

```text
Fabric / ADLS Gen2
  -> preparación de datos y features
  -> Azure ML job / pipeline
  -> modelo registrado
  -> endpoint online o batch
  -> Foundry agent / app / dashboard
```

Mensajes que conviene reforzar:

- Fabric ya está cubierto como plataforma de datos y analítica.
- Azure ML se encarga del ciclo de vida de modelos predictivos.
- Foundry consume capacidades y conocimiento para crear experiencias generativas y agentes.
- La integración debe respetar identidad, permisos, linaje, trazabilidad y coste.
- Si Foundry indexa datos de Fabric/OneLake mediante una knowledge base, Azure AI Search necesita identidad manejada y permisos explícitos sobre el origen.
- Foundry también necesita permisos sobre Azure AI Search o sobre la conexión que usa la knowledge base.

## 11. Checklist antes de impartir

- [ ] Proyecto Foundry abre correctamente.
- [ ] Dos modelos desplegados responden en playground.
- [ ] Variables locales documentadas.
- [ ] Knowledge base indexada y con citas.
- [ ] Identidad manejada habilitada en Azure AI Search si la knowledge base usa OneLake.
- [ ] Permisos concedidos a Azure AI Search sobre Fabric/OneLake.
- [ ] Permisos concedidos a Foundry sobre Azure AI Search/knowledge base.
- [ ] Agente `agent-aurora-soporte` creado.
- [ ] Preguntas de aceptación probadas.
- [ ] Hay al menos una traza con tool call.
- [ ] Hay al menos una traza de rechazo por seguridad.
- [ ] Evaluación preparada o capturas disponibles.
- [ ] Workspace Azure ML abre correctamente.
- [ ] Compute instance y cluster preparados.
- [ ] Data asset `aurora-incidencias` registrado.
- [ ] Dos runs MLflow disponibles.
- [ ] Modelo `aurora-prioridad-incidencia` registrado.
- [ ] Endpoint online, batch endpoint o capturas de respaldo preparadas.
- [ ] Slides PDF/PPTX generadas.
- [ ] Capturas de respaldo listas para demos críticas.
- [ ] Costes revisados y recursos con límites claros.

## 12. Limpieza posterior

Al terminar el curso:

1. Exportar evidencias o capturas que se quieran conservar.
2. Eliminar agentes de prueba de alumnos si están en el tenant del formador.
3. Borrar índices no usados de Azure AI Search.
4. Revisar Application Insights y retención de conversaciones.
5. Parar compute instances de Azure ML.
6. Eliminar endpoints online si no se van a reutilizar.
7. Parar o eliminar recursos con coste no deseado.
