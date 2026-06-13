# Notebook PySpark · Monitorización de drift (Aurora Energía)

> Contenido del notebook `07-drift-monitor` del [Ejercicio 7 de Jornada 3](../../../ejercicios/jornada-3/ej07-monitorizacion-drift.md).

---

## Celda 1 · PSI helper

```python
import numpy as np

def psi(expected, actual, buckets: int = 10) -> float:
    """Population Stability Index entre dos arrays numéricos."""
    bps = np.quantile(expected, np.linspace(0, 1, buckets + 1))
    bps[0], bps[-1] = -np.inf, np.inf
    e, _ = np.histogram(expected, bps)
    a, _ = np.histogram(actual, bps)
    e_p = np.clip(e / e.sum(), 1e-6, None)
    a_p = np.clip(a / a.sum(), 1e-6, None)
    return float(((a_p - e_p) * np.log(a_p / e_p)).sum())
```

## Celda 2 · Cargar baseline (training) y producción (últimos 7 días)

```python
from pyspark.sql import functions as F
import pandas as pd

df_all = spark.read.table("features_demanda_horaria")

cutoff = df_all.agg(F.max("ts_hora")).first()[0]
baseline_max = pd.Timestamp(cutoff) - pd.Timedelta(days=35)
prod_min     = pd.Timestamp(cutoff) - pd.Timedelta(days=7)

baseline = df_all.filter(F.col("ts_hora") <= F.lit(baseline_max)).toPandas()
prod     = df_all.filter(F.col("ts_hora") >  F.lit(prod_min)).toPandas()
```

## Celda 3 · PSI por feature

```python
features = ["lag_24h", "avg_24h", "temperatura", "viento_kmh"]
rows = []
for f in features:
    rows.append({
        "feature": f,
        "psi": psi(baseline[f].dropna().values, prod[f].dropna().values),
        "evaluado_en": pd.Timestamp.utcnow(),
    })

df_psi = spark.createDataFrame(pd.DataFrame(rows))
df_psi.show()
```

## Celda 4 · MAPE rolling 7 días

```python
from sklearn.metrics import mean_absolute_percentage_error

df_pred = spark.read.table("gold.forecast_demanda") \
    .filter(F.col("ts_hora") > F.lit(prod_min)).toPandas()
df_real = spark.read.table("fact_ventas") \
    .filter(F.col("categoria_producto") == "electricidad") \
    .withColumn("ts_hora", F.date_trunc("hour", "fecha_venta")) \
    .groupBy("estacion_id", "ts_hora").agg(F.sum("kwh").alias("kwh_real")) \
    .filter(F.col("ts_hora") > F.lit(prod_min)).toPandas()

joined = df_pred.merge(df_real, on=["estacion_id", "ts_hora"], how="inner")
mape_7d = mean_absolute_percentage_error(joined["kwh_real"], joined["kwh_pred"])
print(f"MAPE 7d = {mape_7d:.4f}")
```

## Celda 5 · Persistir salud del modelo

```python
import pandas as pd

health = pd.DataFrame([{
    "feature":     "_global",
    "psi":         float(df_psi.agg(F.max("psi")).first()[0]),
    "mape_7d":     mape_7d,
    "evaluado_en": pd.Timestamp.utcnow(),
}])

(spark.createDataFrame(pd.concat([health, df_psi.toPandas().assign(mape_7d=None)], ignore_index=True))
    .write.format("delta").mode("append").saveAsTable("gold.model_health"))
```

## Celda 6 · Salida para pipeline (exit value)

```python
import json
veredicto = {
    "psi_max": float(df_psi.agg(F.max("psi")).first()[0]),
    "mape_7d": mape_7d,
    "reentrenar": (df_psi.agg(F.max("psi")).first()[0] > 0.25) or (mape_7d > 0.15),
}
mssparkutils.notebook.exit(json.dumps(veredicto))
```
