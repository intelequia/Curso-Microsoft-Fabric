# AML-M1 · Qué es Azure Machine Learning Studio

**Duración:** 30 min · **Formato:** explicación + demo corta

## Objetivos

1. Entender Azure Machine Learning Studio como portal de trabajo para ciencia de datos y MLOps.
2. Diferenciar Azure ML Studio, Microsoft Foundry y Microsoft Fabric.
3. Identificar las piezas principales: workspace, datos, compute, jobs, modelos, endpoints y monitorización.

## Hilo narrativo

> "Foundry nos ayuda a construir aplicaciones y agentes de IA generativa. Azure ML Studio nos ayuda a entrenar, versionar, desplegar y operar modelos predictivos y personalizados."

## Contenido

Azure Machine Learning Studio es la experiencia web de Azure Machine Learning. Desde el portal se gestionan datasets, notebooks, compute, experimentos, pipelines, modelos, endpoints, métricas, seguridad y gobierno del ciclo de vida ML.

### Componentes principales

| Pieza | Para qué sirve |
| --- | --- |
| **Workspace** | Contenedor de recursos, activos, historial y configuración de Azure ML. |
| **Studio** | Portal web para trabajar con notebooks, jobs, AutoML, Designer, modelos y endpoints. |
| **Datastore / data asset** | Conexión y versionado lógico de datos usados por jobs y pipelines. |
| **Compute instance** | Máquina interactiva para notebooks y exploración. |
| **Compute cluster** | Clúster escalable para jobs, AutoML y pipelines. |
| **Environment** | Imagen y dependencias reproducibles para ejecutar entrenamiento o inferencia. |
| **Job / experiment** | Ejecución trazable con parámetros, métricas, artefactos y logs. |
| **Model registry** | Registro de modelos y versiones. |
| **Endpoint** | Superficie gestionada para inferencia online o batch. |

### Azure ML Studio vs Foundry vs Fabric

| Plataforma | Encaje principal |
| --- | --- |
| **Microsoft Foundry** | Aplicaciones generativas, agentes, herramientas, knowledge, evaluación generativa y operación de agentes. |
| **Azure Machine Learning Studio** | Ciencia de datos, entrenamiento, AutoML, MLflow, registro, endpoints, batch scoring y MLOps. |
| **Microsoft Fabric** | Datos, lakehouse, pipelines analíticos, notebooks de Fabric, BI y experiencias de Data Science integradas en Fabric. |

Regla práctica: si necesitas entrenar, comparar y desplegar un modelo predictivo propio, usa Azure ML. Si necesitas un agente que razona, usa herramientas y responde con lenguaje natural, usa Foundry. Si el problema empieza en datos corporativos y analítica, Fabric suele ser el origen o destino natural.

## Demo en vivo

1. Abrir `https://ml.azure.com`.
2. Entrar en el workspace `mlw-aurora-curso`.
3. Mostrar la navegación: Notebooks, Jobs, Data, Models, Endpoints, Environments y Compute.
4. Comparar visualmente con `https://ai.azure.com`.
5. Dibujar el flujo objetivo: Fabric/Storage -> Azure ML -> endpoint/modelo -> Foundry/app.

## Mensajes clave

- Azure ML Studio no sustituye Foundry: cubre otra parte del ciclo de vida de IA.
- El workspace es la unidad operativa de Azure ML.
- Un proyecto serio de ML necesita datos, compute, tracking, registro, despliegue y monitorización.
