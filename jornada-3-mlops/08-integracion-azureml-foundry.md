# J3-M8 · Cuándo salir de Fabric: Azure ML y Azure AI Foundry

**Duración:** 15 min · **Formato:** explicación + Q&A · **Pre-requisito:** ninguno adicional

## Objetivos

1. Reconocer los **límites** del stack ML nativo de Fabric.
2. Saber cuándo apoyarse en **Azure Machine Learning** (entrenamiento distribuido GPU, endpoints online, AutoML avanzado).
3. Saber cuándo apoyarse en **Azure AI Foundry** (LLMs, agentes, fine-tuning, modelos fundacionales).
4. Diseñar patrones híbridos donde Fabric es la **plataforma de datos** y Azure ML/Foundry los **motores de cómputo especializados**.

## Hilo narrativo

> "Fabric resuelve el 80% de los casos de ML empresariales en analítica clásica. Para el 20% restante — visión, NLP profundo, LLMs custom, *online serving* de baja latencia — el patrón ganador es **datos en Fabric, cómputo en Azure ML o Foundry**, y los resultados de vuelta a OneLake."

## Contenido

### 1. Qué hace Fabric muy bien

- Analítica tabular clásica: regresión, clasificación, clustering, series temporales.
- Scoring batch sobre datos en Lakehouse / Warehouse.
- Scoring streaming con latencia 10–60 s.
- Experimentación MLflow integrada con el lake.
- Gobierno extremo a extremo con Purview.

### 2. Cuándo subir a Azure ML

| Necesidad | Por qué Azure ML |
| --- | --- |
| Entrenamiento **distribuido multi-GPU** | Compute clusters con A100/H100, PyTorch DDP, DeepSpeed |
| **Online serving** < 100 ms | Managed online endpoints con autoescalado |
| **AutoML** maduro (visión, NLP, forecasting con cientos de modelos) | Producto nativo |
| **Responsible AI dashboard** completo | Componentes oficiales (fairness, error analysis, counterfactuals) |
| **CLI/SDK v2** con MLOps GitOps avanzado | `az ml` + jobs como YAML, pipelines DAG |

Integración con Fabric:

- Datos leídos directamente de OneLake vía **conectores nativos** o montaje de ADLS Gen2 subyacente.
- Modelos registrados en Azure ML pueden **invocarse desde Fabric** vía REST o como tarea de Pipeline.
- Métricas y predicciones devueltas a tablas Delta en OneLake para cierre del bucle.

### 3. Cuándo subir a Azure AI Foundry

| Necesidad | Por qué Foundry |
| --- | --- |
| **LLMs gestionados** (GPT-4o, GPT-4.1, o-series, Llama, Mistral) | Catálogo y endpoint listos |
| **Agentes** con tools, function calling, memoria | Agent Service |
| **Fine-tuning** de modelos fundacionales | Pipeline gestionado SFT/DPO/RFT |
| **Evaluación** de calidad de outputs LLM (groundedness, safety) | Evaluators integrados |
| **Búsqueda vectorial** sobre documentos corporativos | Azure AI Search + integraciones |

Integración con Fabric:

- **Fabric IQ Data Agents** usan modelos servidos en Foundry por debajo.
- Documentos curados en OneLake → indexados en AI Search → consumidos por agentes Foundry.
- Trazas de agentes pueden aterrizar como tablas Delta para analítica.

### 4. Patrón híbrido recomendado para Aurora Energía

```
        ┌─────────────────────────────────────┐
        │           OneLake (Fabric)          │
        │  raw · silver · features · gold     │
        └───────┬──────────────┬──────────────┘
                │              │
   training GPU │              │ scoring online
                ▼              ▼
        ┌──────────────┐  ┌──────────────────┐
        │  Azure ML    │  │ Azure AI Foundry │
        │ - LightGBM   │  │ - GPT-4.1        │
        │ - PyTorch    │  │ - Agents         │
        │ - Endpoints  │  │ - Fine-tuning    │
        └──────┬───────┘  └─────────┬────────┘
               │                    │
               └────────► predictions / responses ──► OneLake (gold)
```

### 5. Reglas de decisión rápidas

- ¿Cabe en una sesión Spark de Fabric en horas razonables? → **Fabric**.
- ¿Necesito *online* < 100 ms con SLA? → **Azure ML endpoint**.
- ¿Es un LLM? → **Foundry**, salvo casos triviales con Azure OpenAI.
- ¿Lo va a operar un equipo SQL / BI? → **Fabric** (sin duda).
- ¿Lo va a operar un equipo ML Engineering con CI/CD GitHub? → híbrido **Fabric + Azure ML**.

### 6. Lo que NO recomendamos

- ❌ Replicar datos enteros de OneLake a un storage de Azure ML — usar **conectores** o **mount**.
- ❌ Reentrenar en Azure ML y registrar en MLflow de Azure ML *y* en Fabric — elegir un único registro y enlazarlo desde el otro.
- ❌ Ignorar Purview cuando el modelo se sirve en Azure ML — propagar etiquetas y linaje vía Purview connectors.

## Mensajes clave

- "Fabric no compite con Azure ML/Foundry — **se complementan**."
- "El **dato vive en OneLake**. El cómputo va donde haga falta."
- "Decide por **carga de trabajo y equipo operativo**, no por moda."

> **Siguiente módulo (M9):** ponemos en práctica la integración con Foundry construyendo el *Aurora Insight Agent* — un agente que consume las predicciones de los modelos ML y genera briefings operacionales publicados en Teams. Ver [09-agente-ia-foundry-fabric.md](09-agente-ia-foundry-fabric.md).
