# J3-M5 · Scoring en tiempo real con Real-Time Intelligence y Activator

**Duración:** 25 min · **Formato:** demo en vivo · **Pre-requisito:** Eventhouse `eh_aurora_telemetria` de Jornada 1

## Objetivos

1. Combinar **Eventstream**, **Eventhouse** y un modelo de ML para hacer scoring de baja latencia.
2. Entrenar el modeo de predicción sacando los datos del eventsteam.
3. Desplegar el modelo para hacer inferencia online en microbatch.
4. Mostrar cómo Fabric permite pasar de datos en streaming a acciones operativas casi en tiempo real.

## Hilo narrativo

> "El equipo de operaciones de la flota de bicicletas quiere anticiparse al estado de las bicis casi en tiempo real, sin esperar a procesos batch. A partir de la telemetría que entra por Eventstream, entrenamos un modelo con histórico, lo desplegamos dentro de Fabric y generamos predicciones en microbatch en menos de un minuto."

## Contenido

### 1. Arquitectura objetivo

```
Bicicletas / sensores IoT
   │  (evento JSON de telemetría)
   ▼
Eventstream  ──►  Eventhouse (KQL DB)   [retención corta, hot data]
   │
   ├─► Stream → Notebook Spark Structured Streaming
   │            │  llama a la api del  modelo MLflow @champion
   │            │  predice cada microbatch
   │            ▼
   │       Tabla Delta `gold.bikes_predictions`
   │
   └─► Activator → alerta a Teams si la predicción supera un umbral
```

### 2. Entrenamiento del detector (offline)

- Modelo: **RandomForest** usando la api de spark.
- Features: las construidas en M2 (`features_ebikes_availability`).
- Entrenado contra histórico de 6 meses, registrado como `mdl_auroroa_ebikes_availability`.

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline

classifier = RandomForestClassifier(
    n_estimators=200,
    max_depth=12,
    min_samples_leaf=2,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1,
)

model_pipeline = Pipeline(steps=[("preprocessor", preprocessor), ("classifier", classifier)])

### 3. Scoring streaming

```python
pdf_events = df_microbatch.toPandas()

responses = []
headers = {"Content-Type": "application/json"}
payload = {
	"BikepointID": str(row.get("BikepointID", row.get("bikepoint_id", ""))),
	"Street": str(row.get("Street", row.get("street", ""))),
	"Neighbourhood": str(row.get("Neighbourhood", row.get("neighbourhood", ""))),
	"Latitude": float(row.get("Latitude", row.get("latitude", 0.0))),
	"Longitude": float(row.get("Longitude", row.get("longitude", 0.0)))
}

event_timestamp = str(row.get(ts_col, datetime.now(timezone.utc).isoformat()))

resp = requests.post(scoring_api_url, json=payload, headers=headers, timeout=10)

```

### 4. Activator (Data Activator)

Ejemplo de trigger
- si risk_score > 0.8
- si prediction = 1

Acción
alerta a Teams al equipo de operaciones
opcionalmente, abrir tarea de reequilibrado o revisión

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
2. Ver el pipeline de entrenamiento con el registro de los modelos, desplegar la ultima versión para hacer inferencia online.
3. Ejecutar el notebook `09-inference-ebikes-availability` en modo microbatch.
4. Ver el `anomaly_score` aparecer en `gold.fraude_scored` y la alerta en el canal de Teams.

## Mensajes clave

- "Real-Time Intelligence + MLflow + Activator = **detección en < 1 min sin desplegar nada nuevo**."
- "El truco es **un único módulo de features** compartido entre offline y online."
- "Fabric llega hasta ~10 s de latencia. Por debajo, integra con Azure ML."
