# J1-M4 · Notebooks, Spark y procesamiento de datos

**Duración:** 35 min · **Formato:** explicación + demo en vivo

## Objetivos

1. Entender el papel de los **Notebooks** en Fabric.
2. Conocer **Spark Pools, Environments y Sessions**.
3. Manejar las APIs básicas: **PySpark, Spark SQL, sparklyr (R)**.
4. Crear un Notebook que transforme `bronze → silver` sobre `lh_aurora`.

## Contenido

### 1. Notebooks en Fabric

- Editor estilo Jupyter con celdas de código y markdown.
- Lenguajes soportados: **PySpark (Python)**, **Spark SQL**, **Scala**, **SparkR / sparklyr**.
- Conexión nativa a uno o varios **Lakehouses** mediante el panel izquierdo "Explorer".
- Ejecución sobre **Apache Spark gestionado** (no hay que provisionar cluster).

### 2. Spark gestionado en Fabric

- **Starter Pool**: pool predeterminado, listo en segundos.
- **Custom pools**: tamaño, autoscale, librerías.
- **Environments**: paquetes Python/Java + configuración Spark + recursos. Versionables y compartibles.
- **Session**: ejecución activa. Se puede dejar **caliente** (high concurrency) entre celdas y notebooks.

### 3. APIs

- **PySpark**: `spark.read.format("csv")`, `df.write.format("delta").saveAsTable(...)`, `df.groupBy(...).agg(...)`.
- **Spark SQL**: en celda con `%%sql`. Útil para alumnos que vienen de SQL puro.
- **NotebookUtils** (`mssparkutils` y `notebookutils`): acceso a OneLake, secretos, fs, jobs encadenados.
- **Pandas API on Spark** y **fabric-data-functions**: lectura de Lakehouse como DataFrame pandas-like.

### 4. Acceso a OneLake desde Spark

```python
# Lectura de tabla del Lakehouse adjunto
df = spark.read.table("lh_aurora.clientes")

# Lectura de fichero en Files/
df_raw = spark.read.option("header", True).csv("Files/landing/ventas.csv")

# Escritura como tabla Delta
df_silver.write.mode("overwrite").format("delta").saveAsTable("ventas_silver")
```

### 5. Caso Aurora Energía: bronze → silver

Notebook `nb_aurora_lab` que:

1. Lee `clientes`, `productos`, `estaciones` y `ventas_raw` del Lakehouse.
2. Limpia `ventas_raw`: quita filas con `importe <= 0`, normaliza fechas, deriva `año`, `mes`, `dia_semana`.
3. Hace join con `productos` para añadir `categoria`, `unidad_medida`.
4. Escribe `ventas_silver` como tabla Delta.

### 6. Buenas prácticas

- Pinear celdas markdown al principio explicando objetivo, inputs y outputs.
- Usar `display(df)` en lugar de `df.show()` para visuales interactivos en Fabric.
- Habilitar **Git integration** en el workspace para versionar notebooks.
- Convertir notebooks "estables" en **Spark Job Definition** para invocarlos desde Pipeline en producción.
- Para grandes volúmenes, **particionar Delta** por columna de baja cardinalidad (ej. año).

## Demo en vivo (15 min)

1. Abrir `nb_aurora_lab` (o crear nuevo). Adjuntar Lakehouse `lh_aurora`.
2. Ejecutar la primera celda con `spark.sql("SELECT COUNT(*) FROM clientes").show()`.
3. Cargar `ventas_raw` en DataFrame, mostrar `display(df)` y comentar el visual.
4. Aplicar transformaciones (filtro, derivadas, join).
5. Escribir `ventas_silver`.
6. Cambiar a celda `%%sql` y mostrar `SELECT año, SUM(importe) FROM ventas_silver GROUP BY año`.
7. Mostrar el **Job History** del Notebook.

## Ejercicios para casa relacionados

- [ej04-notebook-bronze-silver.md](../ejercicios/jornada-1/ej04-notebook-bronze-silver.md)

## Mensajes clave

- "Spark en Fabric es gestionado y de pago por uso real (la capacidad ya lo cubre)."
- "Notebook es la herramienta de transformación más potente — pero no la única."
- "Convierte notebooks estables en Spark Job Definitions y orquéstalos con Pipeline."
