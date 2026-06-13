# Ejercicio 5 (Jornada 3) · Fraude en tiempo real con SynapseML y Activator

**Tiempo estimado:** 60 min · **Modalidad:** fuera de aula

## Objetivo

Entrenar un IsolationForest, desplegarlo sobre streaming y disparar alertas Teams vía Activator.

## Requisitos previos

- CSV `transacciones_fidelizacion.csv` cargado en `Files/raw/` (ejercicio 1).
- Eventstream `es_aurora_telemetria` operativo (Jornada 1).

## Pasos

### Parte A · Entrenamiento offline

1. Crea el notebook `05-fraude-synapseml` (referencia: [assets/ml/notebooks/05-fraude-synapseml.ipynb.md](../../assets/ml/notebooks/05-fraude-synapseml.ipynb.md)).
2. Construye `features_cliente_fraude` con velocity, spread geográfico, ratio importe, horario atípico.
3. Entrena `IsolationForest` de SynapseML con `contamination=0.01`.
4. Regístralo como `mdl_aurora_fraude_iforest` y asigna alias `champion`.

### Parte B · Streaming

5. Crea (o reutiliza) un **Eventstream** `es_aurora_transacciones`:
   - Source: Custom App (mock con notebook que envía 100 eventos/min).
   - Destination: Eventhouse + Custom endpoint para Spark.
6. Crea notebook `06-fraude-stream` con `readStream` desde el Eventstream y aplica el modelo como UDF.
7. Escribe a tabla Delta `gold.fraude_scored` con `anomaly_score` y `modelo_version`.

### Parte C · Activator

8. Crea un **Reflex** (Data Activator) → `act_fraude_alerta`:
   - Object: transacción.
   - Property: `anomaly_score` (sobre `gold.fraude_scored` o Eventstream).
   - Trigger: `score > 0.7`.
   - Action: enviar tarjeta adaptativa a un canal de Teams `#aurora-antifraude`.
9. Lanza el script generador de eventos con 3 transacciones forzadamente anómalas y comprueba que la alerta llega.

## Entregable

- Modelo registrado.
- Tabla `gold.fraude_scored` con > 1.000 filas.
- Captura de la tarjeta Teams recibida.

## Validación

- ✅ Streaming sin errores durante al menos 5 min.
- ✅ Activator `Active` y con histórico de triggers.
- ✅ Latencia evento → alerta < 90 s (medido con `processing_time`).
