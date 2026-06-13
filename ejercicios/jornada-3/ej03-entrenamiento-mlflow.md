# Ejercicio 3 (Jornada 3) · Entrenamiento y registro con MLflow

**Tiempo estimado:** 60 min · **Modalidad:** fuera de aula

## Objetivo

Entrenar 3 modelos de forecast, comparar runs en MLflow y promover el campeón.

## Requisitos previos

- Tabla `features_demanda_horaria` del ejercicio 2.

## Pasos

1. Crea el experimento desde la UI: **+ New → Experiment** → `exp_aurora_forecast_demanda`.
2. Crea el notebook `03-train-forecast-mlflow` (referencia: [assets/ml/notebooks/03-train-forecast-mlflow.ipynb.md](../../assets/ml/notebooks/03-train-forecast-mlflow.ipynb.md)).
3. Implementa:
   - **Split temporal**: últimas 4 semanas como validación, resto como training (NO usar split aleatorio).
   - **Modelo 1 (baseline)**: predecir `lag_168h`. Loguear como run `baseline_naive`.
   - **Modelo 2 (Prophet)**: bucle sobre 5 estaciones piloto, MAPE medio. Loguear como run `prophet_v1`.
   - **Modelo 3 (LightGBM)**: 4 combinaciones de hiperparámetros con `mlflow.autolog()`.
4. Para cada run, loguea:
   - Métricas `mae`, `mape`, `rmse`.
   - Tag `feature_version="v1.0"`.
   - `mlflow.log_input` con la tabla `features_demanda_horaria`.
5. En la UI del Experiment:
   - Ordena por `mape` ascendente.
   - Selecciona el mejor LightGBM → **Register model** → `mdl_aurora_forecast_demanda`.
6. Asigna alias `champion` a la versión registrada (UI o `MlflowClient`).

## Entregable

- Captura del Experiment con los runs ordenados por MAPE.
- Captura del ML Model con la versión y el alias `champion` visible.

## Validación

- ✅ Al menos 6 runs en el experimento.
- ✅ Modelo registrado con al menos 1 versión.
- ✅ Alias `champion` asignado.
- ✅ Tabla `features_demanda_horaria` aparece como **input dataset** del run ganador.
