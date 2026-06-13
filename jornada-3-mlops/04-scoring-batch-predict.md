# J3-M4 · Despliegue y scoring batch con `PREDICT`

**Duración:** 30 min · **Formato:** demo guiada · **Pre-requisito:** modelo `mdl_aurora_forecast_demanda@champion` registrado en M3

## Objetivos

1. Entender la función **`PREDICT`** y dónde se puede invocar (PySpark sobre Lakehouse y T-SQL sobre Warehouse).
2. Construir un **Pipeline programado** que ejecute la inferencia diaria y materialice resultados en una tabla gold.
3. Exponer las predicciones a Power BI vía **Direct Lake** sin pasos adicionales.
4. Evitar los antipatrones más comunes (re-entrenar en el mismo job, hard-codear versiones, mezclar inferencia con features).

## Hilo narrativo

> "El modelo ya está registrado. Negocio quiere ver mañana en su dashboard de Power BI **la demanda esperada para las próximas 48 h por estación**. No queremos endpoint, no queremos servidor: queremos una **tabla**."

## Contenido

### 1. `PREDICT` en PySpark

```python
from synapse.ml.predict import MLFlowTransformer

scorer = MLFlowTransformer(
    inputCols=feature_cols,
    outputCol="kwh_pred",
    modelName="mdl_aurora_forecast_demanda",
    modelVersion="champion",   # alias
)

df_scored = scorer.transform(df_features_futuro)
```

### 2. `PREDICT` en T-SQL (Warehouse)

```sql
SELECT
    estacion_id,
    ts_hora,
    p.kwh_pred
FROM PREDICT(
    MODEL = 'mdl_aurora_forecast_demanda',
    DATA  = dbo.v_features_demanda_futuro AS d
) WITH (kwh_pred FLOAT) AS p;
```

> Útil cuando el equipo "dueño" del pipeline es de **BI / SQL** y no de Spark.

### 3. Materialización gold y refresco

- Tabla destino: `gold.forecast_demanda` con `estacion_id`, `ts_hora`, `kwh_pred`, `modelo_version`, `scoring_run_id`, `scored_at`.
- **Sobrescribir partición** del día (`mode="overwrite"` + `replaceWhere`) en vez de truncar toda la tabla.
- Recoger `modelo_version` real desde `mlflow.MlflowClient().get_model_version_by_alias(...).version` y guardarla en la fila.

### 4. Orquestación con Data Pipeline

Secuencia diaria 06:00 (ver ejercicio EJ3-04):

1. **Notebook**: refresco de `features_demanda_horaria` para las próximas 48 h (con clima previsto).
2. **Notebook**: inferencia con `PREDICT` y escritura a `gold.forecast_demanda`.
3. **Stored Procedure**: refresco de tabla de KPIs en Warehouse.
4. **Semantic Model refresh** (opcional — Direct Lake no lo necesita, pero un *framing* manual fuerza la actualización del cache).
5. **Teams notification** (Activity) con resumen de filas procesadas y MAPE vs. real del día anterior.

### 5. Power BI Direct Lake

- Añadir `gold.forecast_demanda` al modelo semántico `sm_aurora_ventas`.
- Crear medidas `Demanda real`, `Demanda prevista`, `Error %`.
- Visual de línea: real vs. previsto por estación → **el negocio ya puede consumirlo sin saber que existe un modelo**.

### 6. Antipatrones a evitar

- ❌ Entrenar y scorer en el mismo notebook diario.
- ❌ Hard-codear `modelVersion="3"` (rompe el A/B y dificulta rollback).
- ❌ Re-generar todas las features históricas cada día (sólo las del horizonte de predicción + ventana de lags).
- ❌ Sobrescribir la tabla gold completa cuando sólo cambian las próximas 48 h.

## Demo en vivo (10 min)

1. Mostrar el Pipeline `pl_forecast_demanda_diario` y sus 5 actividades.
2. Ejecutarlo manualmente y seguir la pestaña *Run history*.
3. Abrir SQL endpoint y consultar `gold.forecast_demanda`.
4. Refrescar el dashboard de Power BI y mostrar la nueva visual.

## Mensajes clave

- "En Fabric, **el endpoint del modelo es una tabla**. Ese es el cambio mental."
- "`PREDICT` desacopla *quién entrena* de *quién consume* — el SQL Developer no necesita saber Python."
- "Scoring batch + Direct Lake = **producción de ML sin DevOps de servidores**."
