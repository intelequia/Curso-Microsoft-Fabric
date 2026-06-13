# Notebook PySpark · Features de demanda horaria (Aurora Energía)

> Contenido del notebook `02-features-demanda` del [Ejercicio 2 de Jornada 3](../../../ejercicios/jornada-3/ej02-feature-engineering-demanda.md). Adjunta `lh_aurora_ml` y `env_aurora_ml`.

---

## Celda 1 · Cargar ventas eléctricas a granularidad horaria

```python
from pyspark.sql import functions as F

df_ventas = spark.read.table("fact_ventas").filter(F.col("categoria_producto") == "electricidad")

df_demanda = (
    df_ventas
    .withColumn("ts_hora", F.date_trunc("hour", F.col("fecha_venta")))
    .groupBy("estacion_id", "ts_hora")
    .agg(F.sum("kwh").alias("kwh"))
)
df_demanda.show(5)
```

## Celda 2 · Cargar clima histórico

```python
df_clima_raw = (spark.read
    .option("header", True).option("inferSchema", True)
    .csv("Files/raw/clima_historico.csv"))

df_clima = (df_clima_raw
    .withColumn("ts_hora", F.to_timestamp("ts_hora"))
    .select("estacion_id", "ts_hora", "temperatura", "viento_kmh", "precipitacion_mm"))

df_clima.write.format("delta").mode("overwrite").saveAsTable("clima_horario")
```

## Celda 3 · Lags y rolling windows

```python
from pyspark.sql import Window

w_lag    = Window.partitionBy("estacion_id").orderBy("ts_hora")
w_roll24 = w_lag.rowsBetween(-23, -1)

df_feat = (
    df_demanda
    .withColumn("lag_1h",   F.lag("kwh", 1).over(w_lag))
    .withColumn("lag_24h",  F.lag("kwh", 24).over(w_lag))
    .withColumn("lag_168h", F.lag("kwh", 168).over(w_lag))
    .withColumn("avg_24h",  F.avg("kwh").over(w_roll24))
    .withColumn("std_24h",  F.stddev("kwh").over(w_roll24))
)
```

## Celda 4 · Calendario + join clima

```python
df_feat = (df_feat
    .withColumn("hora",   F.hour("ts_hora"))
    .withColumn("dow",    F.dayofweek("ts_hora"))
    .withColumn("mes",    F.month("ts_hora"))
    .withColumn("anio",   F.year("ts_hora"))
    .withColumn("es_pico", F.col("hora").between(18, 22).cast("int"))
    .join(df_clima, ["estacion_id", "ts_hora"], "left")
    .dropna(subset=["lag_168h"])
)
df_feat.printSchema()
```

## Celda 5 · Metadatos y escritura

```python
df_out = (df_feat
    .withColumn("feature_version", F.lit("v1.0"))
    .withColumn("generado_en",     F.current_timestamp()))

(df_out.write
    .format("delta")
    .mode("overwrite")
    .partitionBy("anio", "mes")
    .option("overwriteSchema", "true")
    .saveAsTable("features_demanda_horaria"))

print(f"Filas escritas: {df_out.count():,}")
```

## Celda 6 · Documentación de columnas (SQL)

```sql
%%sql
ALTER TABLE features_demanda_horaria ALTER COLUMN lag_168h COMMENT 'kWh observados hace 168h (misma hora semana anterior)';
ALTER TABLE features_demanda_horaria ALTER COLUMN avg_24h  COMMENT 'Media móvil de kWh en las últimas 24h';
ALTER TABLE features_demanda_horaria ALTER COLUMN es_pico  COMMENT 'Indicador de franja pico 18:00–22:00';

DESCRIBE EXTENDED features_demanda_horaria;
```
