# Notebook PySpark · Fraude con SynapseML IsolationForest (Aurora Energía)

> Contenido del notebook `05-fraude-synapseml` del [Ejercicio 5 de Jornada 3](../../../ejercicios/jornada-3/ej05-fraude-realtime-activator.md).

---

## Celda 1 · Cargar transacciones y construir features

```python
from pyspark.sql import functions as F, Window

df_tx = (spark.read
    .option("header", True).option("inferSchema", True)
    .csv("Files/raw/transacciones_fidelizacion.csv")
    .withColumn("ts", F.to_timestamp("ts")))

w_24h = Window.partitionBy("cliente_id").orderBy(F.col("ts").cast("long")).rangeBetween(-86400, -1)
w_1h  = Window.partitionBy("cliente_id").orderBy(F.col("ts").cast("long")).rangeBetween(-3600,  -1)
w_hist = Window.partitionBy("cliente_id")

df_feat = (df_tx
    .withColumn("tx_count_1h",  F.count("*").over(w_1h))
    .withColumn("tx_count_24h", F.count("*").over(w_24h))
    .withColumn("prov_unique_24h", F.size(F.collect_set("provincia").over(w_24h)))
    .withColumn("avg_importe_hist", F.avg("importe").over(w_hist))
    .withColumn("ratio_importe", F.col("importe") / F.col("avg_importe_hist"))
    .withColumn("hora", F.hour("ts"))
    .withColumn("horario_atipico", F.col("hora").between(2, 5).cast("int"))
    .na.fill({"tx_count_1h": 0, "tx_count_24h": 0, "prov_unique_24h": 1, "ratio_importe": 1.0}))

df_feat.write.format("delta").mode("overwrite").saveAsTable("features_cliente_fraude")
```

## Celda 2 · Vectorizar features

```python
from pyspark.ml.feature import VectorAssembler

FEAT_COLS = ["tx_count_1h", "tx_count_24h", "prov_unique_24h",
             "ratio_importe", "horario_atipico", "importe"]

assembler = VectorAssembler(inputCols=FEAT_COLS, outputCol="features")
df_train = assembler.transform(spark.read.table("features_cliente_fraude")).select("features")
```

## Celda 3 · Entrenar IsolationForest

```python
import mlflow
from synapse.ml.isolationforest import IsolationForest

mlflow.set_experiment("exp_aurora_fraude")

with mlflow.start_run(run_name="iforest_v1"):
    iforest = (IsolationForest()
        .setNumEstimators(200)
        .setContamination(0.01)
        .setFeaturesCol("features")
        .setPredictionCol("anomaly_score"))

    model = iforest.fit(df_train)
    mlflow.spark.log_model(model, "model",
        registered_model_name="mdl_aurora_fraude_iforest")
    mlflow.log_params({"n_estimators": 200, "contamination": 0.01})
```

## Celda 4 · Promocionar a champion

```python
from mlflow.tracking import MlflowClient
client = MlflowClient()
v = client.get_latest_versions("mdl_aurora_fraude_iforest")[0]
client.set_registered_model_alias("mdl_aurora_fraude_iforest", "champion", v.version)
```

## Celda 5 · Scoring streaming (notebook 06-fraude-stream)

```python
from pyspark.sql.types import StructType, StringType, DoubleType, TimestampType

schema = (StructType()
    .add("tx_id", StringType()).add("ts", TimestampType())
    .add("cliente_id", StringType()).add("estacion_id", StringType())
    .add("provincia", StringType()).add("importe", DoubleType()))

stream_raw = (spark.readStream
    .format("eventhubs")
    .options(**eh_opts)
    .load()
    .selectExpr("CAST(body AS STRING) as json")
    .select(F.from_json("json", schema).alias("e"))
    .select("e.*"))

stream_feat = (stream_raw
    .withColumn("hora", F.hour("ts"))
    .withColumn("horario_atipico", F.col("hora").between(2, 5).cast("int"))
    # NOTA: en streaming algunas features históricas se aproximan o se
    # consultan contra una tabla estado materializada. Simplificado en demo.
    .withColumn("tx_count_1h", F.lit(0))
    .withColumn("tx_count_24h", F.lit(0))
    .withColumn("prov_unique_24h", F.lit(1))
    .withColumn("ratio_importe", F.lit(1.0)))

stream_scored = assembler.transform(stream_feat)

import mlflow.pyfunc
model_uri = "models:/mdl_aurora_fraude_iforest@champion"
scorer = mlflow.pyfunc.spark_udf(spark, model_uri)

stream_out = stream_scored.withColumn("anomaly_score",
    scorer(F.struct(*FEAT_COLS))).withColumn("modelo_version", F.lit(v.version))

(stream_out.writeStream
    .format("delta")
    .option("checkpointLocation", "Files/_chk/fraude")
    .outputMode("append")
    .trigger(processingTime="30 seconds")
    .toTable("gold.fraude_scored"))
```
