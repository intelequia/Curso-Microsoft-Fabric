---
marp: true
theme: intelequia
paginate: true
size: 16:9
title: "Jornada 3 · MLOps en Microsoft Fabric"
description: "Master class de 4 horas: del dato gobernado al modelo en producción — Data Science, MLflow, scoring batch y streaming, gobierno, drift y reentrenamiento"
author: Intelequia
math: katex
---

<!-- _class: lead bare -->

<span class="tag">Curso · Jornada 3 de 3</span>

# **MLOps** sobre Microsoft Fabric
## Del dato gobernado al modelo en producción

### 4 horas · master class · caso *Aurora Energía*

<!--
Bienvenida a la Jornada 3. Tras dos jornadas centradas en datos y gobierno, hoy convertimos los datos en decisiones predictivas. Preguntar a la sala: ¿cuántos tienen ya modelos de ML en producción hoy? ¿En qué plataforma? Esa respuesta da el termómetro. El hilo conductor sigue siendo Aurora Energía: hoy abordamos 3 casos reales — forecast, disponibilidad de e-bikes y segmentación. La meta no es enseñar ML (eso son meses), sino enseñar cómo se opera ML en Fabric de forma productiva y gobernada.
-->

---

## Repaso exprés de J1 y J2

- **J1**: construimos el flujo `CSV → Lakehouse → Spark → Warehouse → Power BI Direct Lake` con tiempo real KQL.
- **J2**: aplicamos Purview (Data Map, Catalog, Sensitivity, DLP) e introducimos Data Agents.
- Hoy la pregunta es:

> ¿Cómo pasamos del *qué pasó* al **qué va a pasar** y al **qué es raro**, sin perder gobierno ni reproducibilidad?

<!--
Recordar a los alumnos que el workspace y las tablas que construyeron las dos jornadas anteriores se reutilizan hoy tal cual — no hay que rehacer nada. Si alguien no completó los ejercicios para casa, el tenant compartido auroraenergiasl.onmicrosoft.com tiene un workspace 'aurora-curso-ml-ref' con el estado base ya cargado.
-->

---

## El reto de Aurora Energía · 3 casos de ML

| Caso | Tipo | Por qué importa |
|---|---|---|
| **Forecast demanda eléctrica horaria** | Regresión / series temporales | Compras al mercado mayorista |
| **Disponibilidad de e-bikes (Bicycles)** | Clasificación (multiclase) | Planificaciones de recarga, micro-batch < 15 min |
| **Segmentación B2B logística** | Clustering | Campañas personalizadas |

> Cubrimos las **tres familias** clásicas y todo el **ciclo MLOps** en 4 horas.

<!--
Esta tabla es el mapa mental de la jornada. Aunque hagamos demos sobre el caso de forecast principalmente, los conceptos aplican a los tres. La clave es que los tres comparten infraestructura, gobierno y patrón operativo en Fabric. Si alguien pregunta por casos más exóticos (NLP, visión, LLMs custom) → lo dejamos para el bloque M8 donde hablamos de Azure ML y Foundry.
-->

---

## Agenda · 4 h con descanso de 15 min

| Bloque | Min | Tema |
|---|---|---|
| **M0** | 15 | Repaso + presentación de los 3 casos |
| **M1** | 25 | Fundamentos Data Science en Fabric |
| **M2** | 35 | Feature engineering a escala |
| **M3** | 40 | Experimentación con MLflow |
| ☕ | 15 | **Descanso** |
| **M4** | 30 | Scoring batch con `PREDICT` |
| **M5** | 25 | Ingesta streaming y scoring micro-batch |
| **M6** | 25 | Gobierno con Purview + Fabric IQ |
| **M7** | 25 | Monitorización, drift y reentrenamiento |
| **M8** | 15 | Cuándo salir a Azure ML / Foundry |
| **M9** | 30 | Del modelo al agente: Foundry + Fabric |
| **M10** | 10 | Cierre y deberes |

<!--
Mismo patrón que J1 y J2: bloques cortos + demos en vivo + descanso a mitad. M1-M3 cubren la fase de construcción. M4-M5 la de despliegue. M6-M7 la de operación gobernada. M8 el outlook hacia fuera de Fabric. M9 materializa la integración con un agente real sobre Foundry + Fabric. M10 el cierre con los deberes.
-->

---

<!-- _class: section -->

<span class="module">M1 · 25 min</span>

# Data Science en Fabric
## La experiencia, los runtimes y los Environments

<!--
Transición. Empezamos por las piezas básicas: dónde vive el código, con qué runtime corre, cómo se gestiona la reproducibilidad. La idea fuerza es que Data Science en Fabric NO es Azure ML — vive dentro del mismo workspace que el resto del estack analítico.
-->

---

## La experiencia Data Science

- Acceso desde el *app switcher* → **Data Science**.
- Items específicos: **Notebook**, **Experiment**, **ML Model**, **Environment**.
- **Comparte capacidad y permisos** con el resto de items del workspace.
- Integración nativa con **MLflow** (no se instala — se usa).
- Lee directamente tablas Delta de OneLake → **sin copias**.

> El científico de datos vive en el mismo workspace que el ingeniero y que el analista BI.

<!--
Insistir: cero billing aparte, cero infraestructura propia, cero copias de datos. Para una organización que ha sufrido data sprawl con Databricks + Azure ML + ADF, esto es liberador. Para una que ya tiene Azure ML maduro, es complementario: Fabric para los casos analíticos clásicos, Azure ML para los pesados.
-->

---

## Runtimes y Environments

**Runtimes disponibles:**
- **PySpark** (datasets grandes, joins distribuidos)
- **Python puro** / pandas (prototipado, training scikit-learn)
- **R** (estadística clásica)
- **GPU pools** opcionales (según SKU)

**Environments:**
- Artefacto del workspace que fija **runtime + paquetes + Spark properties**.
- Se adjunta a notebooks y Spark Job Definitions → **reproducibilidad** Dev/Test/Prod.
- Alternativa a `%pip install` en producción.

<!--
Mostrar en vivo cómo se crea un Environment en el bloque demo de M1: añadir prophet y lightgbm, publicar, esperar a Ready. Insistir en que NUNCA se debe depender de '%pip install' en pipelines productivos — eso lo veremos en M7 cuando hablemos de Deployment Pipelines.
-->

---

## Librerías que vais a usar hoy

**Tabular clásico:** scikit-learn, LightGBM, XGBoost, CatBoost
**Series temporales:** Prophet, statsmodels
**Deep learning:** PyTorch, TensorFlow (CPU; GPU según SKU)
**Distribuido sobre Spark:** SynapseML (LightGBM, IsolationForest, Cognitive Services)
**MLOps:** MLflow (integrado), Data Wrangler, Copilot for DS

> **Pista:** SynapseML es vuestro mejor amigo cuando los datos no caben en memoria.

<!--
SynapseML viene preinstalado y es un superpoder real: convierte algoritmos clásicos (LightGBM, IsolationForest) en versiones distribuidas sobre Spark sin que cambie casi la API. En Aurora Energía lo usamos en M5 para entrenamiento y procesado a escala de datos del stream. Copilot for Data Science (en preview o GA según región) genera celdas a partir de prompt — útil pedagógicamente pero SIEMPRE revisar el código antes de ejecutar.
-->

---

<!-- _class: section -->

<span class="module">M2 · 35 min</span>

# Feature engineering
## Tratar las features como producto

<!--
Transición al bloque más práctico. La tesis: un modelo sin feature engineering reproducible es un cuaderno bonito. La diferencia entre experimento y producto está aquí. Las features son artefactos de primera clase, con esquema, versión, comentarios, linaje en Purview y pipeline de refresco.
-->

---

## Feature store ligero sobre OneLake

- Una **tabla Delta por caso** (`features_forecast_demanda_horaria`, `features_ebikes_availability`, `features_b2b_segmentacion`).
- Columnas técnicas: `feature_version`, `generado_en`, `pipeline_run_id`.
- **Documentadas** con `COMMENT` SQL → visibles en SQL endpoint y Purview.
- **Time travel Delta** = snapshot reproducible: `VERSION AS OF` para re-entrenar como hace 30 días.

> Sin producto adicional, sin licencias extra. **OneLake + Delta = feature store básico.**

<!--
Vendido como diferenciador: muchas plataformas obligan a comprar un feature store como producto (Feast, Tecton, Databricks Feature Store). Fabric te da el 80% de la funcionalidad gratis si aplicas la disciplina: una tabla por caso, naming consistente, time travel para re-entrenamiento reproducible. El 20% que falta (online lookup de baja latencia) lo veremos en M5 / M8.
-->

---

## Features de series temporales · forecast demanda

```python
from pyspark.sql import functions as F, Window

w_lag    = Window.partitionBy("estacion_id").orderBy("ts_hora")
w_roll24 = w_lag.rowsBetween(-23, -1)

df_feat = (df_demanda
    .withColumn("lag_24h",  F.lag("kwh", 24).over(w_lag))
    .withColumn("lag_168h", F.lag("kwh", 168).over(w_lag))
    .withColumn("avg_24h",  F.avg("kwh").over(w_roll24))
    .withColumn("hora",     F.hour("ts_hora"))
    .withColumn("es_pico",  F.col("hora").between(18, 22).cast("int"))
    .join(df_clima, ["estacion_id", "ts_hora"], "left")
    .dropna(subset=["lag_168h"]))
```

<!--
Mostrar en vivo este código en el notebook 02-features-demanda. La regla de oro: el mismo notebook genera features para training y para scoring — solo cambia el rango de fechas. Si tienes dos códigos distintos, tienes un bug latente (training-serving skew).
-->

---

## Regla de oro del feature engineering

> El **mismo código** que genera features de **training** debe generar las de **inferencia**.

- Si tienes dos códigos → tienes un **bug latente** (*training-serving skew*).
- Encapsula en un módulo Python en el Environment.
- Parametriza por **rango de fechas**, no por entorno.

<!--
Esta es la lección más cara de aprender en producción. El 70% de los modelos que fallan silenciosamente en producción es por training-serving skew: el dato que llega al modelo no se preprocesa igual que el que se usó para entrenarlo. Encapsular las features en un módulo Python compartido (que vive en el Environment) elimina el problema.
-->

---

<!-- _class: section -->

<span class="module">M3 · 40 min</span>

# Experimentación con MLflow
## El registro como memoria del equipo

<!--
Transición. Si M2 era el qué entra al modelo, M3 es cómo trackeamos qué probamos, qué funcionó y qué se promovió. Fabric integra MLflow nativamente: Experiments y ML Models son items de primera clase.
-->

---

## Tracking, registry, deployment

| Pieza MLflow | Item Fabric | Para qué |
|---|---|---|
| Tracking server | **Experiment** | Runs: params, metrics, artifacts |
| Model registry | **ML Model** | Versiones y aliases (`@champion`, `@challenger`) |
| Deployment | `PREDICT` + Pipelines | Sin endpoint dedicado |

> En Fabric, **registry y deployment están desacoplados**: registra una vez, sirve donde quieras (batch, streaming, T-SQL).

<!--
La novedad de los aliases reemplazando a los stages (Staging/Production/Archived) ya está consolidada. Los aliases son flexibles: champion para producción, challenger para A/B, shadow para evaluar nuevos modelos sin afectar usuarios. Permite tener varios 'alias-stages' personalizados según el equipo lo necesite.
-->

---

## Anatomía de un run

```python
import mlflow
mlflow.set_experiment("exp_aurora_forecast_demanda")

with mlflow.start_run(run_name="lgbm_v1"):
    mlflow.log_params({"n_estimators": 800, "max_depth": 8})
    model = train_lgbm(X_train, y_train)
    mlflow.log_metrics({
        "mae":  mean_absolute_error(y_valid, model.predict(X_valid)),
        "mape": mean_absolute_percentage_error(y_valid, model.predict(X_valid)),
    })
    mlflow.log_input(mlflow.data.from_pandas(X_train, source="features_demanda_horaria"))
    mlflow.lightgbm.log_model(model, "model",
        registered_model_name="mdl_aurora_forecast_demanda")
```

<!--
Tres cosas obligatorias: log_params, log_metrics, log_input. La última es la que da el linaje en Purview: enlaza el run con la tabla Delta de features. Sin log_input no hay linaje a nivel de dataset. mlflow.log_input es relativamente reciente, asegúrate de la versión.
-->

---

## Promoción y aliases

```python
client = mlflow.MlflowClient()
client.set_registered_model_alias(
    name="mdl_aurora_forecast_demanda",
    alias="champion",
    version=3,
)

# Desde otro notebook
model = mlflow.pyfunc.load_model(
    "models:/mdl_aurora_forecast_demanda@champion"
)
```

> **Nunca hardcodees** `version=3`. Carga siempre por alias.

<!--
Este es el patrón que permite rollback instantáneo: si el nuevo champion da problemas, basta con reasignar el alias a la versión anterior. Sin tocar pipelines, sin redeploys. Es la equivalencia funcional al blue/green deployment para modelos.
-->

---

<!-- _class: section -->

<span class="module">M4 · 30 min</span>

# Scoring batch con `PREDICT`
## El endpoint del modelo es una tabla

<!--
Cambio de bloque tras el descanso. Ya tenemos modelo registrado. Ahora lo ponemos en producción. La idea provocadora: en Fabric el endpoint es una tabla Delta, no una API REST. Eso cambia cómo se diseña y se consume.
-->

---

## `PREDICT` en PySpark y en T-SQL

```python
from synapse.ml.predict import MLFlowTransformer

scorer = MLFlowTransformer(
    inputCols=feature_cols, outputCol="kwh_pred",
    modelName="mdl_aurora_forecast_demanda",
    modelVersion="champion")

df_scored = scorer.transform(df_features_futuro)
```

```sql
SELECT estacion_id, ts_hora, p.kwh_pred
FROM PREDICT(
    MODEL = 'mdl_aurora_forecast_demanda',
    DATA  = dbo.v_features_demanda_futuro AS d
) WITH (kwh_pred FLOAT) AS p;
```

<!--
Mostrar ambas en vivo. El SQL es lo que más sorprende a la audiencia tradicional de BI: pueden invocar modelos sin saber Python. Para un equipo donde los data engineers son SQL-first, esto es un game-changer.
-->

---

## Pipeline diario `pl_forecast_demanda_diario`

1. Refresco incremental de **features** próximas 48 h.
2. Scoring con `PREDICT` → `gold.forecast_demanda`.
3. Stored procedure de KPIs en Warehouse.
4. *(opcional)* refresh framing del modelo semántico.
5. Notificación Teams con resumen.

Consumido por Power BI **Direct Lake** sin paso intermedio.

> El negocio ve la predicción **como cualquier otro KPI**.

<!--
Es el mismo pipeline que verán en EJ3-04. Subrayar el patrón overwrite con replaceWhere para no sobrescribir todo cada día. Y la métrica del MAPE del día anterior en la notificación: cierra el bucle entre operación y calidad. Sin eso, nadie se entera de que el modelo se está degradando hasta que el dashboard hace cosas raras.
-->

---

<!-- _class: section -->

<span class="module">M5 · 25 min</span>

# Streaming e Inferencia Micro-batch
## Ingesta continua, reentrenamiento y alertas

<!--
Cambio de caso de uso: ahora hablamos del modelo de disponibilidad de e-bikes (Bicycles). La arquitectura combina Real-Time Intelligence de J1 con MLflow de M3 y Data Activator. Los datos se ingestan continuamente en streaming y se usan como histórico para reentrenar en offline, pero ejecutamos la inferencia en micro-batch (cada 5-15 min) consumiendo una API REST externa porque no es viable hacerlo en streaming directo/continuo de alta frecuencia.
-->

---

## Arquitectura · ingesta streaming + scoring micro-batch

```
Estaciones IoT (e-bikes) ──► Eventstream ──► Eventhouse / Lakehouse (bicycles)
                                                    │
             ┌──────────────────────────────────────┘
             │  (datos del stream para reentrenar)
             ▼
      Feature Pipeline (Gold)
             │
             ▼
   MLflow Model Registry  ──► API REST (Web App)
                                   ▲
                                   │  (peticiones POST micro-batch)
      Inferencia Micro-batch ──────┘  Notebook nb-09-inference
             │
             ▼
    Delta `gold.predictions_ebikes_availability`
             │
             ▼
    Data Activator ──► Alerta / Acción en Teams
```

- Ingestión continua en **tiempo real** en OneLake (tabla `bicycles` de Bronce).
- **Reentrenamiento**: Se extrae el dataset histórico originado del streaming para reentrenamiento offline.
- **Scoring en Micro-batch** (cada 5–15 min): Invocación HTTP POST a la API REST de scoring para calificar la disponibilidad de bicicletas.
- **Activator** = trigger **no-code** si la disponibilidad de bicis o anclajes libres es baja (`LOW_BIKES` / `LOW_DOCKS`).

<!--
Demo en vivo: ejecutar el notebook nb-09-inference-ebikes-availability para procesar eventos recientes de bicicletas de los últimos 15 min e invocar la API REST de scoring. Mostrar la latencia de las peticiones HTTP y cómo se insertan los resultados en gold.predictions_ebikes_availability, disparando la alerta de Activator si baja de cierto umbral.
-->

---

## Cuándo hacer scoring Micro-batch vs. Streaming

| Patrón | Latencia / Cadencia | Caso de Uso |
|---|---|---|
| **Batch diario** | Diaria / Horaria | Forecast de demanda mayorista, reportes BI |
| **Micro-batch** | Cada 5–15 min | **Disponibilidad de e-bikes**. Llamadas a APIs externas, evitar caídas de red, volumen controlado de eventos recientes |
| **Streaming puro** | Segundos (NRT) | Telemetría IoT inmediata, detección de anomalías con Spark Structured Streaming |
| **Baja Latencia Crítica** | < 100 ms | Decisión transaccional síncrona en tiempo real → **Azure ML / API Online** |

> **Lección:** Cuando la inferencia consume una API externa, el scoring **micro-batch** es el patrón ideal para evitar bloquear la ingesta.

<!--
Esto es la transición conceptual hacia M8. Si la sala pregunta 'pero entonces ¿cuándo Azure ML?' la respuesta corta es: cuando necesitas online serving < 100ms, GPU dedicada para entrenamiento o LLMs. Para todo lo demás, Fabric es suficiente y más simple.
-->

---

<!-- _class: section -->

<span class="module">M6 · 25 min</span>

# Gobierno de ML
## Purview + Fabric IQ

<!--
Bloque crítico. Sin gobierno, ML en producción es deuda técnica con disfraz de innovación. Hoy enlazamos lo de la J2 (Purview, Sensitivity, Data Agents) con los modelos que acabamos de construir.
-->

---

## Linaje extremo a extremo en Purview

```
dim_cliente ─┐
fact_ventas ─┼─► features_demanda ─► exp_forecast ─► mdl_forecast@champion
clima_hist ──┘                                              │
                                                            ▼
                                              gold.forecast ─► sm_aurora ─► Reporte
```

- Capturado por Purview al escanear el tenant Fabric.
- **Etiquetas de sensibilidad** se propagan automáticamente.
- DLP puede bloquear features con PII fuera de su tabla origen.

<!--
Mostrar en vivo el grafo de linaje en Purview. Subir desde el modelo hasta los CSVs originales y bajar hasta el reporte Power BI. Ese grafo es lo que necesita auditoría para responder '¿qué datos generaron esta predicción?'. Sin él, ML en producción es indefendible.
-->

---

## Responsible AI checklist mínimo

- [ ] **Model card** documentada por modelo en producción.
- [ ] **Fairness** por grupo sensible (provincia, segmento) reportado.
- [ ] **Plan de retirada** definido.
- [ ] **Owner humano** identificable (no "el equipo").
- [ ] **Etiqueta de sensibilidad** asignada y propagada.
- [ ] **Aprobación** del Deployment Pipeline registrada.

> Sin estos 6 puntos, **no se sube a Prod**.

<!--
Esta es la slide que más os van a fotografiar. Es práctica, accionable, defensible ante auditoría. Si vuestra organización no tiene aún un comité de Responsible AI, este checklist es un buen punto de partida para crearlo. La sensibilidad y el owner son las dos más olvidadas y las más críticas.
-->

---

## Data Agent que explica predicciones

`agt_aurora_forecast` con:
- Fuentes: `gold.forecast_demanda` + `gold.demanda_real`.
- Glosario: "demanda", "previsión", "error", "hora pico".
- Instrucción: **citar `modelo_version` y `scored_at`** en cada respuesta.

> *"¿En qué estaciones el modelo se equivoca más esta semana?"* → tabla con citas verificables.

<!--
La gracia del Data Agent sobre predicciones no es que invente — es que da una capa conversacional sobre datos gobernados. La instrucción de citar modelo_version es clave: convierte respuestas conversacionales en respuestas auditables. Si la respuesta tiene cita, se puede verificar.
-->

---

<!-- _class: section -->

<span class="module">M7 · 25 min</span>

# Monitorización y reentrenamiento
## El reloj empieza cuando el modelo entra a prod

<!--
Bloque operativo. Después del despliegue empieza el verdadero MLOps. Tres tipos de drift, métricas, dashboard, pipeline condicional, Deployment Pipelines. La idea fuerza: reentrenar a evidencia, no a calendario.
-->

---

## Tres tipos de drift

| Tipo | Qué cambia | Cómo se detecta |
|---|---|---|
| **Data drift** | Distribución de features | PSI, KS, χ² |
| **Concept drift** | Relación X → y | Caída de MAPE / AUC |
| **Service drift** | Latencia, errores, rango | Logs del pipeline |

> Medir las tres. Confundirlas lleva a diagnósticos equivocados.

<!--
Ejemplo real: caída de MAPE puede deberse a data drift (cambian los inputs) o concept drift (cambia la realidad). El primero se arregla reentrenando con el dataset actualizado. El segundo puede requerir cambiar features o incluso el algoritmo. Confundirlas → reentrenas y reentrenas sin que mejore.
-->

---

## Pipeline `pl_reentrenamiento_forecast`

1. Notebook de **monitorización** (PSI + MAPE).
2. **If**: `PSI > 0.25 OR MAPE_7d > umbral`.
3. → Feature refresh + training → **`challenger`**.
4. **A/B test** challenger vs. champion últimos 7 días.
5. Si gana → invocar **Deployment Pipeline** para promover.
6. Notificación Teams con veredicto.

> Reentrenar **a evidencia**, no a calendario.

<!--
El umbral PSI > 0.25 es convencional pero arbitrario — ajustarlo a vuestro contexto. Lo crítico es que la decisión de reentrenar sea automatizable y trazable, no manual. Y que la promoción a champion solo ocurra si el A/B lo justifica. Esto evita el antipatrón de 'reentrenar cada noche por si acaso' que consume capacidad sin valor.
-->

---

## Deployment Pipelines Dev → Test → Prod

- Tres workspaces: `aurora-ml-dev`, `aurora-ml-test`, `aurora-ml-prod`.
- Propaga notebooks, environments, modelos, pipelines.
- **Reglas por entorno**: alias del modelo, connection strings, nombres de tablas.
- **Aprobación humana** al promover a Prod.
- Promoción **auditada** y **reversible**.

<!--
La aprobación humana NO es burocracia — es el punto donde se valida el Responsible AI checklist de M6. Sin ese gate, el pipeline de reentrenamiento podría poner en producción un modelo con sesgo no detectado. Subrayar reversible: si tras la promoción algo va mal, basta reasignar el alias champion a la versión anterior. Cero downtime.
-->

---

<!-- _class: section -->

<span class="module">M8 · 15 min</span>

# Cuándo salir de Fabric
## Azure ML y Azure AI Foundry

<!--
Bloque corto, conceptual, honesto. Fabric resuelve la mayoría de los casos analíticos clásicos pero no todos. Aquí mostramos cuándo apoyarse en Azure ML (entrenamiento GPU pesado, online serving, AutoML maduro) y cuándo en Azure AI Foundry (LLMs, agentes, fine-tuning). El dato sigue en OneLake.
-->

---

## Reglas rápidas de decisión

| Pregunta | Respuesta |
|---|---|
| ¿Cabe en sesión Spark en horas razonables? | **Fabric** |
| ¿Necesito online < 100 ms con SLA? | **Azure ML endpoint** |
| ¿Es un LLM? | **Foundry** |
| ¿Equipo SQL/BI lo opera? | **Fabric** sin duda |
| ¿Equipo ML Eng con GitOps maduro? | Híbrido **Fabric + Azure ML** |

> El **dato vive en OneLake**. El **cómputo va donde haga falta**.

<!--
La frase final es la que os tenéis que llevar. Decidir por carga de trabajo y por equipo operativo, no por moda. He visto equipos meter LLMs custom en Databricks porque 'es lo que sabemos' cuando Foundry lo resolvía en una tarde. Y he visto equipos forzar todo en Foundry cuando un LightGBM en Fabric resolvía el problema con menor coste.
-->

---

<!-- _class: section -->

<span class="module">M9 · 30 min</span>

# Del modelo al agente
## Aurora Insight Agent con Foundry + Fabric

<!--
Este es el módulo que cierra el bucle. Hasta ahora hemos construido modelos, los hemos puesto en producción y monitorizado. Pero la pregunta del negocio es: ¿y quién consume estas predicciones? ¿Quién las interpreta? La respuesta es un agente de IA que traduce predicciones en decisiones. Y lo construimos con integración nativa: Fabric Data Agent como fuente de datos gobernada, Foundry Agent Service como orquestador con razonamiento.
-->

---

## El gap: de predicción a decisión

| Hoy (M1-M7) | Con agente (M9) |
|---|---|
| Tabla Gold → Power BI → humano interpreta | Tabla Gold → **Agente** → briefing + acciones |
| Activator → alerta simple Teams | Agente → alerta **contextualizada** + causa raíz |
| Drift → notebook manual | Agente → diagnóstico + **recomendación automática** |

> El agente **no reemplaza** los modelos — los consume, interpreta y traduce a acción.

<!--
Preguntar a la sala: ¿cuántos de vuestros modelos en producción generan un output que alguien realmente lee y actúa? La mayoría de los modelos mueren en una tabla Gold que nadie mira. El agente es la última milla que faltaba.
-->

---

## Arquitectura: dos capas integradas

```
┌─────────────────────────────────────────┐
│  Azure AI Foundry Agent Service         │
│  aurora-insight-agent (GPT-4.1-mini)    │
│  ├─ FabricTool → Data Agent Fabric      │
│  ├─ FunctionTool: analizar_drift()      │
│  └─ FunctionTool: generar_recomendacion │
└──────────────┬──────────────────────────┘
               │ identity passthrough (OBO)
┌──────────────▼──────────────────────────┐
│  Microsoft Fabric                       │
│  Data Agent: agt_aurora_insights        │
│  ├─ gold.forecast_demanda               │
│  ├─ gold.predictions_ebikes_availability │
│  ├─ gold.metricas_drift                 │
│  └─ Gobierno: RLS + Labels + Purview    │
└─────────────────────────────────────────┘
```

<!--
Dos capas, no una. El Fabric Data Agent da acceso gobernado a los datos (con RLS, sensitivity labels, todo lo que vimos en J2). El Foundry Agent añade la capa de razonamiento: interpreta, cruza datos, llama a funciones custom y genera el briefing. La integración es nativa vía FabricTool — no es un hack, es un conector oficial del SDK azure-ai-projects.
-->

---

## Capa 1: Fabric Data Agent

- **Mismo patrón de J2-M6**, pero sobre tablas de predicciones:
  - `gold.forecast_demanda` · `gold.predictions_ebikes_availability` · `gold.metricas_drift`
- Instrucciones ajustadas para **devolver datos estructurados** (JSON/tablas)
- Few-shot examples orientados a métricas ML
- Se **publica** → genera `workspace_id` + `artifact_id`

> El Data Agent es el **punto de acceso gobernado** — RLS, labels y lineage aplican.

<!--
Nada nuevo conceptualmente respecto a J2. La novedad es que las fuentes ahora son tablas de predicciones ML, no tablas de ventas. Mismo gobierno, misma seguridad, mismo patrón.
-->

---

## Capa 2: Foundry Agent con FabricTool

```python
from azure.ai.agents.models import FabricTool, FunctionTool

# Fabric Data Agent como tool nativo
conn_id = project_client.connections.get("aurora-fabric-connection").id
fabric = FabricTool(connection_id=conn_id)

# Funciones custom para lógica que SQL no cubre
functions = FunctionTool(functions={
    analizar_drift,
    generar_recomendacion
})

agent = agents_client.create_agent(
    model="gpt-4.1-mini",
    name="aurora-insight-agent",
    instructions=SYSTEM_PROMPT,
    tools=fabric.definitions + functions.definitions,
)
```

<!--
El código real. Tres líneas para conectar Fabric como tool, tres más para las funciones custom, y create_agent combina ambos. El modelo gpt-4.1-mini es suficiente para orquestar — no necesitamos GPT-4o completo porque el razonamiento pesado lo hacen las funciones. Coste optimizado.
-->

---

## Function calling: lógica que un SQL no puede hacer

| Función | Qué hace | Por qué no es SQL |
|---|---|---|
| `analizar_drift()` | Tendencia PSI, features afectadas, recomendación | Requiere análisis temporal + umbral + lógica condicional |
| `generar_recomendacion()` | Prioriza acciones según reglas de negocio | Combina múltiples señales (demanda + disponibilidad + drift) |

> El LLM decide **cuándo** llamar cada función basándose en la pregunta del usuario.

<!--
Esto es lo que diferencia un Data Agent de un verdadero agente inteligente. El Data Agent responde 'cuánto'. Las functions responden 'qué hacer al respecto'. Y el LLM orquesta cuándo usar cada cosa. Function calling es el patrón clave — no es el LLM generando SQL, es el LLM decidiendo qué herramienta usar.
-->

---

## Ejemplo: briefing operacional

> *"Dame el briefing de hoy."*

🟡 **Demanda** · Madrid-Sur con 18% error (media 6%). Pico previsto mañana 19h: +22%.

🔴 **Disponibilidad** · Alerta crítica en estación "Estrella". Disponibilidad < 5% estimada en próximas 2 horas.

🔴 **Drift** · Modelo demanda: PSI=0.31 en feature `temperatura`. 3 días sobre umbral.

**Recomendaciones:**
1. ⚡ Activar cargadores auxiliares Madrid-Sur
2. 🚲 Enviar camión de balanceo / reposición a estación "Estrella"
3. 🔄 Reentrenar modelo demanda con datos recientes

<!--
Esto es lo que recibe el director de operaciones a las 7 de la mañana en Teams. Sin abrir Power BI, sin entrar en Fabric, sin mirar notebooks. Un briefing accionable que cruza los tres modelos. Pregunta a la sala: ¿cuánto vale esto vs un dashboard que nadie mira?
-->

---

## Publicación: dónde vive el agente

| Canal | Cómo |
|---|---|
| **API REST** | Endpoint nativo de Foundry → integrable con cualquier sistema |
| **Teams** | Foundry → Publish → Teams app → fijar en canal |
| **Briefing automático** | Logic App (07:00) → POST al agente → Adaptive Card a Teams |
| **Power BI** | Web embed en informe para preguntas ad-hoc |

> **Gobierno**: identity passthrough, RLS heredado, trazas en App Insights.

<!--
La publicación en Teams es la que más impacto tiene para usuarios de negocio. Pero la API es la que permite automatización. La combinación Logic App + agente + Teams es el patrón más potente: briefing diario automático a las 7 de la mañana sin que nadie lo pida.
-->

---

## Mensaje clave M9

> Un modelo en producción sin agente es como un informe que nadie lee.
>
> **La IA generativa cierra el bucle entre predicción y decisión.**

- Fabric Data Agent = acceso **gobernado** a datos
- Foundry Agent = **razonamiento** + tools + publicación
- Juntos, no separados.

<!--
Este es el cierre conceptual de la jornada. Hemos ido de datos crudos a modelos, de modelos a predicciones, de predicciones a un agente que genera decisiones. El ciclo completo en una plataforma integrada.
-->

---

<!-- _class: section -->

# Cierre
## Próximos pasos y deberes

---

## ¿Qué nos llevamos hoy?

- Data Science en Fabric **no es** Azure ML — es complementario y vive en el mismo workspace.
- **OneLake + Delta = feature store básico** sin coste adicional.
- **MLflow es ciudadano de primera clase**: Experiment + ML Model como items.
- **`PREDICT`** elimina el "deployar endpoint" para casos batch / SQL.
- Ingesta streaming + scoring micro-batch + Activator = **alertas automatizadas sin DevOps**.
- Gobierno (**Purview**) y conversacional (**Data Agents**) cierran el círculo.
- Reentrenar **a evidencia**, propagar con **Deployment Pipelines**.
- **IA generativa cierra el bucle**: Foundry Agent + Fabric Data Agent = de predicción a decisión.

---

## Deberes · pack de ejercicios

| Ejercicio | Tema | Tiempo |
|---|---|---|
| EJ3-01 | Workspace + Environment ML | 30 min |
| EJ3-02 | Features de demanda | 45 min |
| EJ3-03 | Training MLflow | 60 min |
| EJ3-04 | Pipeline scoring + Power BI | 45 min |
| EJ3-05 | Ingesta streaming y scoring micro-batch | 60 min |
| EJ3-06 | Deployment Pipeline | 45 min |
| EJ3-07 *(opcional)* | Drift monitor | 60 min |
| EJ3-08 | Aurora Insight Agent (Foundry + Fabric) | 60 min |

> Total: ~6 h. Disponible en `ejercicios/jornada-3/`.

<!--
Avisar: el EJ3-07 es opcional pero el que más diferencia. Si solo van a hacer uno extra, que sea ese — porque integra todo lo aprendido. Recordar el canal de soporte asíncrono para dudas.
-->

---

<!-- _class: lead bare -->

# ¡Gracias!
## Preguntas, debate y siguientes pasos

`https://github.com/intelequia/Curso-Microsoft-Fabric`

<!--
Cierre. Pedir feedback: qué bloque os resultó más útil, cuál más difícil, qué echaríais en falta para una hipotética Jornada 4. Mencionar que el roadmap natural sería: Jornada 4 podría profundizar en LLMs y agentes con Foundry + Fabric, o en un caso vertical (Healthcare / Sustainability con Industry Solutions).
-->
