# Ejercicio 4 (Jornada 1) · Notebook PySpark Bronze → Silver

**Tiempo estimado:** 60 min · **Modalidad:** fuera de aula

## Objetivo

Implementar el patrón medallón (bronze → silver) con un Notebook PySpark anclado al Lakehouse `lh_aurora`.

## Pasos

1. **+ New → Notebook** → `nb_aurora_bronze_silver`.
2. Adjunta el Lakehouse `lh_aurora` como **default lakehouse**.
3. En la primera celda, lee la tabla bronze:

   ```python
   df_ventas_bronze = spark.read.table("fact_ventas_raw")
   df_ventas_bronze.printSchema()
   df_ventas_bronze.show(5)
   ```

4. Aplica las transformaciones a Silver:
   - Filtrar registros con `importe IS NULL OR importe <= 0`.
   - Cast de `fecha_venta` a `timestamp`.
   - Crear columna `anio`, `mes`, `dia`.
   - Lookup con `dim_producto` para añadir `categoria_producto`.
   - Particionar por `anio` y `mes` al guardar.

   ```python
   from pyspark.sql import functions as F
   
   df_prod = spark.read.table("dim_producto")
   
   df_silver = (df_ventas_bronze
       .filter(F.col("importe") > 0)
       .withColumn("fecha_venta", F.to_timestamp("fecha_venta"))
       .withColumn("anio", F.year("fecha_venta"))
       .withColumn("mes", F.month("fecha_venta"))
       .withColumn("dia", F.dayofmonth("fecha_venta"))
       .join(df_prod.select("producto_id", "categoria"), "producto_id", "left")
       .withColumnRenamed("categoria", "categoria_producto")
   )
   
   (df_silver.write
       .format("delta")
       .mode("overwrite")
       .partitionBy("anio", "mes")
       .saveAsTable("fact_ventas"))
   ```

5. Añade una celda final con **calidad básica**:

   ```python
   total_bronze = df_ventas_bronze.count()
   total_silver = spark.read.table("fact_ventas").count()
   print(f"Bronze: {total_bronze}, Silver: {total_silver}, Filtrados: {total_bronze - total_silver}")
   ```

6. Asocia este notebook al pipeline del Ejercicio 3.

## Entregable

- Notebook ejecutado sin errores.
- Captura del schema final y conteo bronze/silver.
- Verificar desde SQL endpoint: `SELECT TOP 5 * FROM fact_ventas`.

## Validación

- ✅ Tabla `fact_ventas` particionada por anio/mes.
- ✅ Sin importes ≤ 0.
- ✅ Columna `categoria_producto` informada.
