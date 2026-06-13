# J3-M3 · Experimentación y registro de modelos con MLflow

**Duración:** 40 min · **Formato:** demo + ejercicio corto en aula · **Pre-requisito:** tabla `features_demanda_horaria` creada en M2

## Objetivos

1. Entender la integración nativa de **MLflow** en Fabric: `Experiment` y `ML Model` como items del workspace.
2. Trackear parámetros, métricas y artefactos de varios runs y compararlos en la UI.
3. **Registrar** el mejor modelo, asignarle alias (`@champion`, `@challenger`) y promocionarlo entre workspaces.
4. Conocer **autologging** y cuándo desactivarlo.

## Hilo narrativo

> "En Aurora Energía vamos a probar tres aproximaciones al forecast: un *baseline naive*, **Prophet** y **LightGBM** con las features que hemos construido. El mejor gana, pero **todos** quedan registrados — porque el día que el campeón se degrade, el challenger ya está esperando."

## Contenido

### 1. Concepto: tracking, registry, deployment

| Pieza MLflow | Pieza Fabric | Para qué |
| --- | --- | --- |
| Tracking server | **Experiment** (item) | Guarda runs: params, metrics, artifacts |
| Model registry | **ML Model** (item) | Versiona modelos, gestiona aliases |
| Deployment | `PREDICT` + Pipelines | Scoring batch/streaming sin endpoint dedicado |

### 2. Estructura típica de un run

```python
import mlflow
from sklearn.metrics import mean_absolute_error

mlflow.set_experiment("exp_aurora_forecast_demanda")

with mlflow.start_run(run_name="lgbm_v1"):
    mlflow.log_params({"n_estimators": 800, "max_depth": 8, "lr": 0.05})

    model = train_lgbm(X_train, y_train, **params)
    preds = model.predict(X_valid)

    mae  = mean_absolute_error(y_valid, preds)
    mape = mean_absolute_percentage_error(y_valid, preds)

    mlflow.log_metrics({"mae": mae, "mape": mape})
    mlflow.lightgbm.log_model(model, artifact_path="model",
                              registered_model_name="mdl_aurora_forecast_demanda")
```

### 3. Autologging

- `mlflow.autolog()` registra automáticamente params, métricas y modelo para sklearn, LightGBM, XGBoost, PyTorch, etc.
- **Cuándo NO usarlo**: entrenamientos largos con muchos folds donde el ruido en la UI estorba; preferir `mlflow.start_run()` explícito por modelo final.

### 4. Comparar runs en la UI

- Item **Experiment** → vista de tabla y gráficos.
- Filtros por parámetros, ordenación por métrica, *parallel coordinates*.
- Botón **Compare** entre 2-5 runs.

### 5. Registrar y promocionar

- `registered_model_name` en `log_model()` crea el item **ML Model** si no existe.
- Cada `log_model` adicional añade una **versión** (v1, v2, v3…).
- **Aliases** (sustituyen a los antiguos *stages*): `@champion`, `@challenger`, `@shadow`.
- Promoción entre entornos = **Deployment Pipeline** (M7).

```python
client = mlflow.MlflowClient()
client.set_registered_model_alias(
    name="mdl_aurora_forecast_demanda",
    alias="champion",
    version=3,
)
```

### 6. Buenas prácticas

- **Un experimento por caso de negocio**, no por persona ni por sprint.
- **Naming**: `exp_<dominio>_<problema>` y `mdl_<dominio>_<problema>`.
- **Tagear** runs con `git_commit`, `dataset_version`, `feature_version`.
- **Loggear el dataset** (`mlflow.log_input`) — Fabric lo enlaza con la tabla Delta para linaje en Purview.
- **No** loguear artefactos de varios GB en cada run.

## Demo en vivo (15 min)

1. Notebook `03-train-forecast-mlflow`.
2. Entrenar baseline naive (predecir = `lag_168h`) y loguearlo.
3. Entrenar **Prophet** por estación (loop sobre 5 estaciones piloto).
4. Entrenar **LightGBM** con grid de 4 combinaciones de hiperparámetros.
5. Abrir el item Experiment, ordenar por MAE, marcar el mejor → **Register** → versión 1.
6. Asignar alias `champion` y mostrar cómo se carga desde otro notebook: `mlflow.pyfunc.load_model("models:/mdl_aurora_forecast_demanda@champion")`.

## Ejercicio corto en aula (5 min)

> Cada alumno añade un run con `n_estimators=1500` y `max_depth=12`. Comparte en chat su MAE. Vemos colectivamente el ranking en la UI del Experiment.

## Mensajes clave

- "El experimento es **la memoria del equipo de ML** — sin él, cada incorporación nueva reinventa la rueda."
- "Alias > stages: refleja mejor las prácticas reales de A/B y shadow deployment."
- "El registry **no despliega** — separa *qué modelo* de *cómo se sirve*."
