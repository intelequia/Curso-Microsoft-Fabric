# J3-M2 · Feature engineering a escala sobre OneLake

**Duración:** 35 min · **Formato:** demo guiada · **Pre-requisito:** Lakehouse `lh_aurora` con tablas silver

## Objetivos

1. Diseñar **feature tables** versionadas como tablas Delta en el Lakehouse.
2. Aplicar transformaciones típicas de ML sobre Spark: *lags*, ventanas móviles, encoding, escalado, calendario.
3. Conocer **Data Wrangler** como acelerador y cómo materializa código reproducible.
4. Entender el patrón **feature store ligero** sobre OneLake (sin producto adicional).

## Hilo narrativo

> "Un modelo es tan bueno como sus features. Y unas features sin contrato, sin versión y sin linaje son **deuda técnica garantizada**. Vamos a tratar las features como un *artefacto de primera clase*: tabla Delta, esquema fijo, documentada en Purview, refrescada por Pipeline."

## Contenido

### 1. ¿Dónde viven las features?

- En el mismo Lakehouse, capa **gold/features**: `lh_aurora_gold.ml_feature.features_*`.
- Convención sugerida:
  - `features_forecast_demanda_horaria` (granularidad: `estacion_id` × `ts_hora`).
  - `features_ebikes_availability` (granularidad: `estacion_id` × `ts_hora`).

### 2. Features de series temporales (caso forecast)

A partir de `fact_ventas` + `clima_historico` (CSV en `assets/ml/data/clima_historico.csv`):

- **Lags**: demanda hace 1 h, 24 h, 168 h (semana).
- **Rolling**: media y desviación últimas 24 h y 7 días.
- **Calendario**: hora del día, día semana, festivos, hora pico sí/no.
- **Clima**: temperatura, viento, precipitación (joineado por `estacion_id` y franja horaria).
- **Categóricas**: provincia, tipo de estación (urbana / autopista / rural).

```python
from pyspark.sql import functions as F, Window

w_lag = Window.partitionBy("estacion_id").orderBy("ts_hora")
w_roll24 = w_lag.rowsBetween(-23, -1)

df_feat = (
    df_demanda
    .withColumn("lag_1h",   F.lag("kwh", 1).over(w_lag))
    .withColumn("lag_24h",  F.lag("kwh", 24).over(w_lag))
    .withColumn("lag_168h", F.lag("kwh", 168).over(w_lag))
    .withColumn("avg_24h",  F.avg("kwh").over(w_roll24))
    .withColumn("std_24h",  F.stddev("kwh").over(w_roll24))
    .withColumn("hora",     F.hour("ts_hora"))
    .withColumn("dow",      F.dayofweek("ts_hora"))
    .withColumn("es_pico",  F.col("hora").between(18, 22).cast("int"))
    .join(df_clima, ["estacion_id", "ts_hora"], "left")
    .dropna(subset=["lag_168h"])
)
```
### 3. Buenas prácticas

- Una **tabla por caso**, no una mega-tabla de features compartida.
- **Documenta cada feature** en su columna (`COMMENT 'lag de 24h en kWh'`) → se ve en SQL endpoint y aparece en Purview.
- Programa el **pipeline de refresco** y registra `pipeline_run_id` para trazabilidad.
- **Nunca calcules features sólo en training**: usa el **mismo notebook/job** para training y para scoring, parametrizado por fecha.

## Demo en vivo (10 min)

1. Abrir notebook `02-features-demanda` adjunto al Lakehouse.
2. Mostrar lectura de `fact_ventas` filtrada a tipo "electricidad".
3. Abrir **Data Wrangler** sobre el DataFrame de clima → aplicar imputación con la media → ver el código generado.
4. Ejecutar la celda de features y mostrar el plan físico de Spark (`df.explain()`) para que vean que es un único job optimizado.
5. Hacer `DESCRIBE HISTORY features_demanda_horaria` en el SQL endpoint para mostrar versiones Delta.

## Mensajes clave

- "Sin feature engineering reproducible no hay MLOps — sólo *modelos en cuaderno*."
- "OneLake + Delta = feature store básico **gratis**: snapshot, versión, linaje."
- "El mismo código que genera features de training **debe** generar las de inferencia."
