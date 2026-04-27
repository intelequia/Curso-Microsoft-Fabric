# Notebook PySpark · Bronze → Silver para Aurora Energía

> Este fichero recoge el contenido del notebook `nb_aurora_bronze_silver` que se construye en el [Ejercicio 4 de Jornada 1](../../ejercicios/jornada-1/ej04-notebook-bronze-silver.md). Cópialo celda a celda en un Notebook de Fabric con el Lakehouse `lh_aurora` adjuntado como default.

---

## Celda 1 · Lectura bronze

```python
df_ventas_bronze = spark.read.table("fact_ventas_raw")
print(f"Filas bronze: {df_ventas_bronze.count():,}")
df_ventas_bronze.printSchema()
df_ventas_bronze.show(5, truncate=False)
```

## Celda 2 · Lookup dimensiones

```python
df_prod = spark.read.table("dim_producto_raw").select("producto_id", "categoria")
df_est  = spark.read.table("dim_estacion_raw").select("estacion_id", "provincia")
```

## Celda 3 · Limpieza + transformación a silver

```python
from pyspark.sql import functions as F

df_silver = (
    df_ventas_bronze
    .filter((F.col("importe").isNotNull()) & (F.col("importe") > 0))
    .withColumn("fecha_venta", F.to_timestamp("fecha_venta"))
    .withColumn("anio", F.year("fecha_venta"))
    .withColumn("mes", F.month("fecha_venta"))
    .withColumn("dia", F.dayofmonth("fecha_venta"))
    .join(df_prod, "producto_id", "left")
    .withColumnRenamed("categoria", "categoria_producto")
    .join(df_est, "estacion_id", "left")
)

df_silver.printSchema()
```

## Celda 4 · Escritura particionada

```python
(
    df_silver.write
        .format("delta")
        .mode("overwrite")
        .partitionBy("anio", "mes")
        .option("overwriteSchema", "true")
        .saveAsTable("fact_ventas")
)
```

## Celda 5 · Validación de calidad

```python
total_bronze = df_ventas_bronze.count()
total_silver = spark.read.table("fact_ventas").count()
descartadas  = total_bronze - total_silver

print(f"Bronze:    {total_bronze:,}")
print(f"Silver:    {total_silver:,}")
print(f"Descartadas: {descartadas:,}  ({descartadas/total_bronze:.2%})")
```

## Celda 6 · KPIs rápidos

```python
display(
    spark.sql("""
        SELECT categoria_producto,
               COUNT(*) AS num_ventas,
               ROUND(SUM(importe), 2) AS importe_total
        FROM fact_ventas
        GROUP BY categoria_producto
        ORDER BY importe_total DESC
    """)
)
```

## Celda 7 (opcional) · Optimización Delta

```python
spark.sql("OPTIMIZE fact_ventas ZORDER BY (fecha_venta, estacion_id)")
spark.sql("VACUUM fact_ventas RETAIN 168 HOURS")
```
