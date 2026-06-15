# J3-M7 · Monitorización, drift y reentrenamiento

**Duración:** 25 min · **Formato:** demo + discusión · **Pre-requisito:** modelo en producción con scoring batch operativo (M4)

## Objetivos

1 - Distinguir data drift, concept drift y degradación de servicio.
2 - Registrar y versionar el dataset de entrenamiento en el Lakehouse, guardándolo en Files.
3 - Implementar métricas de drift en notebooks Fabric con PSI y KS test.
4 - Persistir la monitorización del modelo en el Lakehouse Gold: drift, degradación, predicciones y comparativas contra el target real.
5 - Registrar el control operativo en el Warehouse Gold: ejecuciones de pipelines, estado, errores, métricas relevantes y trazabilidad.
6 - Visualizar la salud del modelo en un dashboard Power BI dedicado.

## Hilo narrativo

> "El día que el modelo entra en producción, el reloj empieza a correr. El mundo cambia, los datos cambian, la verdad cambia. Sin monitorización, un modelo en producción es deuda técnica con apariencia de innovación."

## Contenido

### 1. Tres cosas distintas que llamamos *drift*

| Tipo | Qué cambia | Cómo se detecta |
| --- | --- | --- |
| **Data drift** | Distribución de features de entrada | PSI, KS, χ² entre training y producción |
| **Concept drift** | Relación X → y (el target ya no se comporta igual) | Caída de MAPE / AUC sobre etiquetas frescas |
| **Service drift** | Latencia, errores, valores fuera de rango | Logs del pipeline y de la API |

### 2. Registro y versionado del dataset de entrenamiento
Antes de entrenar un modelo, el dataset usado debe quedar congelado y trazable.
El objetivo es poder responder siempre a:

- Qué datos se usaron para entrenar el modelo.
- Qué versión del dataset corresponde a cada versión del modelo.
- Qué ventana temporal cubría el entrenamiento.
- Qué features y target contenía.
- Qué pipeline/notebook generó ese dataset.
- Dónde está almacenado físicamente.

El dataset de entrenamiento se guarda en el Lakehouse, dentro de Files, versionado por fecha, modelo y ejecución.

Files/
└── ml/
    └── training_datasets/
        └── forecast_demanda/
            └── version=2026-06-15_0743/
                ├── train.parquet
                ├── validation.parquet
                ├── test.parquet
                └── metadata.json

### 3. PSI sobre features (notebook programado)
El drift se calcula comparando la distribución de producción contra la distribución del dataset de entrenamiento registrado.
La referencia no debe ser “la tabla actual”, sino la versión exacta del dataset con la que se entrenó el modelo en producción.
```python
import numpy as np

def psi(expected, actual, buckets=10):
    breakpoints = np.quantile(expected, np.linspace(0, 1, buckets + 1))
    breakpoints[0], breakpoints[-1] = -np.inf, np.inf
    e_counts, _ = np.histogram(expected, breakpoints)
    a_counts, _ = np.histogram(actual,   breakpoints)
    e_perc = np.clip(e_counts / e_counts.sum(), 1e-6, None)
    a_perc = np.clip(a_counts / a_counts.sum(), 1e-6, None)
    return float(((a_perc - e_perc) * np.log(a_perc / e_perc)).sum())
```

Convención de interpretación:

- `PSI < 0.1` → sin drift.
- `0.1 ≤ PSI < 0.25` → drift moderado, vigilar.
- `PSI ≥ 0.25` → drift significativo, reentrenar.

### 4. Métrica de negocio: MAPE rolling

- Sobre `gold.forecast_demanda` y `gold.demanda_real` (cuando llega el real) calculamos MAPE diario, semanal y mensual.
- Visualizado en un reporte Power BI **`Salud del modelo Aurora`** con:
  - Tendencia MAPE últimos 90 días.
  - PSI por feature top-10 (heatmap).
  - % de predicciones generadas por cada versión del modelo (`champion` vs. `challenger`).

### 5. Qué cae en Lakehouse Gold

El Lakehouse Gold es la capa principal para guardar datos analíticos detallados relacionados con el modelo.
Aquí deben caer:

- **Datasets de entrenamiento versionados** en Files.
- **Tablas Delta** con predicciones batch.
- **Resultados detallados** de drift.
- **Métricas de degradación** por periodo.
- **Comparativas** entre predicción y valor real.
- **Evidencias** para reentrenamiento.
- **Información técnica** que pueda ser reutilizada por notebooks, MLflow o análisis posteriores.

Estructura recomendada:

```text
Lakehouse Gold
├── Files/
│   └── ml/
│       └── training_datasets/
│           └── forecast_demanda/
│               └── version=YYYY-MM-DD_HHMM/
│                   ├── train.parquet
│                   ├── validation.parquet
│                   ├── test.parquet
│                   └── metadata.json
│
└── Tables/
    ├── gold.forecast_demanda
    ├── gold.demanda_real
    ├── gold.model_drift_feature
    ├── gold.model_health
    ├── gold.model_prediction_quality
    └── gold.ml_training_dataset_registry
```

### 6. Qué cae en Warehouse Gold

El Warehouse Gold se usa como capa estructurada para control, auditoría, gobierno y reporting operativo.
Aquí deben caer los registros más consumibles por negocio, Power BI, seguimiento de SLAs y control de ejecuciones.
Debe incluir:

- **Ejecuciones** de pipelines.
- **Estado** de notebooks.
- **Duración** de actividades.
- **Errores y mensajes** relevantes.
- **Métricas resumidas** de modelos.
- **Estado final** de cada ciclo de scoring, monitorización o reentrenamiento.
- **Versiones de modelo** usadas.
- **Decisiones tomadas**: mantener champion, promover challenger, lanzar reentrenamiento, etc.

Estructura de tablas:

```text
Warehouse Gold
├── gold.ml.pipeline_execution_log
├── gold.ml.pipeline_activity_log
├── gold.ml.model_execution_summary
├── gold.ml.model_metric_summary
├── gold.ml.model_retraining_decision
└── gold.ml.model_registry_summary
```

### 7. Anti-patrones

- ❌ Reentrenar cada noche "por si acaso" (consumo de capacidad sin retorno).
- ❌ Reemplazar el champion automáticamente sin shadow.
- ❌ Medir sólo precisión técnica y no impacto de negocio.
- ❌ Monitorizar features pero no la **predicción** (`y_hat`) ni el **target real**.

## Demo en vivo (8 min)

1. Ejecutar `07-drift-monitor` y mostrar la tabla `gold.model_health`.
2. Forzar drift inyectando ruido sobre `temperatura` y ver cómo PSI sube por encima de 0.25.
3. Lanzar manualmente `pl_reentrenamiento_forecast` y seguirlo en runs.
4. Mostrar el Deployment Pipeline con la promoción pendiente de aprobación.

## Mensajes clave

- "**Lo que no se mide, no se opera.** Monitorización es parte del producto, no opcional."
- "Reentrenar **a evidencia**, no a calendario."
- "Deployment Pipelines hacen el camino Dev→Test→Prod **reversible y auditable**."
