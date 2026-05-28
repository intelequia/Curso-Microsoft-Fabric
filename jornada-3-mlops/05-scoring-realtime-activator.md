# J3-M5 · Scoring en tiempo real con Real-Time Intelligence y Activator

**Duración:** 25 min · **Formato:** demo en vivo · **Pre-requisito:** Eventhouse `eh_aurora_telemetria` de Jornada 1

## Objetivos

1. Combinar **Eventstream**, **Eventhouse** y un modelo de ML para hacer scoring de baja latencia.
2. Usar **SynapseML** (`IsolationForest`) para entrenar un detector de anomalías sobre transacciones.
3. Disparar alertas con **Activator (Data Activator)** sin código.
4. Entender el límite entre *near real-time* (segundos/minutos) en Fabric y *online serving* (milisegundos) en Azure ML.

## Hilo narrativo

> "El equipo antifraude de Aurora Energía no puede esperar al batch nocturno: cuando una tarjeta se usa de forma sospechosa, quieren saberlo en **menos de 1 minuto**. Lo conseguimos sin salir de Fabric, combinando Real-Time Intelligence con un modelo desplegado como UDF Spark."

## Contenido

### 1. Arquitectura objetivo

```
POS / app móvil
   │  (evento JSON)
   ▼
Eventstream  ──►  Eventhouse (KQL DB)   [retención corta, hot data]
   │
   ├─► Stream → Notebook Spark Structured Streaming
   │            │  carga modelo IsolationForest (MLflow @champion)
   │            │  score cada microbatch
   │            ▼
   │       Tabla Delta `gold.fraude_scored`
   │
   └─► Activator → alerta a Teams si score > umbral
```

### 2. Entrenamiento del detector (offline)

- Modelo: **IsolationForest** de SynapseML, distribuido sobre Spark.
- Features: las construidas en M2 (`features_cliente_fraude`).
- Entrenado contra histórico de 6 meses, registrado como `mdl_aurora_fraude_iforest`.

```python
from synapse.ml.isolationforest import IsolationForest

iforest = (IsolationForest()
    .setNumEstimators(200)
    .setContamination(0.01)
    .setFeaturesCol("features"))

model = iforest.fit(df_train)
mlflow.spark.log_model(model, "model",
    registered_model_name="mdl_aurora_fraude_iforest")
```

### 3. Scoring streaming

```python
from pyspark.sql.functions import col

scorer = mlflow.pyfunc.spark_udf(
    spark, "models:/mdl_aurora_fraude_iforest@champion")

stream = (spark.readStream
    .format("eventhubs")            # o conector Eventstream
    .options(**eh_opts).load()
    .select(parse_event("body").alias("e"))
    .select("e.*")
    .transform(build_features_realtime)      # MISMO código que offline
    .withColumn("anomaly_score", scorer(struct(*feature_cols)))
)

(stream.writeStream
    .format("delta")
    .option("checkpointLocation", "Files/_chk/fraude")
    .outputMode("append")
    .toTable("gold.fraude_scored"))
```

### 4. Activator (Data Activator)

- Objeto **Reflex** que escucha la tabla `gold.fraude_scored` (o directamente el Eventstream con score).
- Definimos:
  - **Object**: transacción.
  - **Property**: `anomaly_score`.
  - **Trigger**: `score > 0.7` durante al menos 1 evento.
  - **Action**: enviar tarjeta adaptativa a un canal de Teams del equipo antifraude.

> Activator es **no-code** — la persona de negocio puede ajustar el umbral sin tocar el notebook.

### 5. Latencia: ¿qué esperar?

| Componente | Latencia típica |
| --- | --- |
| Ingesta Eventstream → Eventhouse | < 5 s |
| Structured Streaming microbatch | 10–60 s (configurable con `trigger`) |
| Activator → Teams | < 5 s tras detección |
| **Total e2e** | **15–90 s** |

> Si necesitas **< 100 ms** (p. ej., bloquear una transacción en el punto de venta), el modelo va a un **endpoint online de Azure ML**, no a Fabric. Lo tratamos en M8.

### 6. Buenas prácticas

- **Reutilizar el código de features** entre offline y online (mismo módulo Python en el Environment).
- **Checkpoint location** siempre fuera de la tabla destino.
- **Versión del modelo** loggeada en cada fila scoreada.
- Probar el **shadow mode**: scorea pero no alerta, durante 1-2 semanas, antes de activar Activator.

## Demo en vivo (8 min)

1. Mostrar el Eventstream `es_aurora_transacciones` y su salida hacia el Eventhouse.
2. Ejecutar el notebook `05-fraude-synapseml` en modo streaming.
3. Inyectar 3 transacciones sintéticas anómalas con `notebookutils`.
4. Ver el `anomaly_score` aparecer en `gold.fraude_scored` y la alerta en el canal de Teams.

## Mensajes clave

- "Real-Time Intelligence + MLflow + Activator = **detección en < 1 min sin desplegar nada nuevo**."
- "El truco es **un único módulo de features** compartido entre offline y online."
- "Fabric llega hasta ~10 s de latencia. Por debajo, integra con Azure ML."
