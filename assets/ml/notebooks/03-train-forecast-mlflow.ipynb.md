# Notebook PySpark · Training forecast con MLflow (Aurora Energía)

> Contenido del notebook `03-train-forecast-mlflow` del [Ejercicio 3 de Jornada 3](../../../ejercicios/jornada-3/ej03-entrenamiento-mlflow.md).

---

## Celda 1 · Carga y split temporal

```python
import pandas as pd
from pyspark.sql import functions as F

df = spark.read.table("features_demanda_horaria").toPandas()
df = df.sort_values(["estacion_id", "ts_hora"])

cutoff = df["ts_hora"].max() - pd.Timedelta(days=28)
train, valid = df[df.ts_hora <= cutoff], df[df.ts_hora > cutoff]
print("Train:", len(train), "Valid:", len(valid))
```

## Celda 2 · Setup MLflow

```python
import mlflow
mlflow.set_experiment("exp_aurora_forecast_demanda")

FEATURES = ["lag_1h", "lag_24h", "lag_168h", "avg_24h", "std_24h",
            "hora", "dow", "es_pico", "temperatura", "viento_kmh", "precipitacion_mm"]
TARGET = "kwh"
```

## Celda 3 · Baseline naive

```python
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error

with mlflow.start_run(run_name="baseline_naive"):
    preds = valid["lag_168h"]
    mae  = mean_absolute_error(valid[TARGET], preds)
    mape = mean_absolute_percentage_error(valid[TARGET], preds)
    mlflow.log_metrics({"mae": mae, "mape": mape})
    mlflow.set_tag("modelo", "baseline")
```

## Celda 4 · Prophet (5 estaciones piloto)

```python
from prophet import Prophet
import numpy as np

estaciones_piloto = train["estacion_id"].drop_duplicates().head(5).tolist()
mapes = []

with mlflow.start_run(run_name="prophet_v1"):
    for est in estaciones_piloto:
        ts_train = train[train.estacion_id == est].rename(columns={"ts_hora": "ds", "kwh": "y"})[["ds", "y"]]
        m = Prophet(daily_seasonality=True, weekly_seasonality=True).fit(ts_train)
        future = valid[valid.estacion_id == est][["ts_hora"]].rename(columns={"ts_hora": "ds"})
        fcst = m.predict(future)["yhat"].values
        y_true = valid[valid.estacion_id == est][TARGET].values
        mapes.append(mean_absolute_percentage_error(y_true, fcst))
    mlflow.log_metric("mape", float(np.mean(mapes)))
    mlflow.set_tag("modelo", "prophet")
```

## Celda 5 · LightGBM con autolog

```python
import lightgbm as lgb

mlflow.lightgbm.autolog()

grid = [
    {"n_estimators": 400,  "max_depth": 6,  "learning_rate": 0.1},
    {"n_estimators": 800,  "max_depth": 8,  "learning_rate": 0.05},
    {"n_estimators": 1500, "max_depth": 10, "learning_rate": 0.03},
    {"n_estimators": 2000, "max_depth": 12, "learning_rate": 0.02},
]

for i, params in enumerate(grid):
    with mlflow.start_run(run_name=f"lgbm_{i}"):
        model = lgb.LGBMRegressor(**params).fit(train[FEATURES], train[TARGET])
        preds = model.predict(valid[FEATURES])
        mlflow.log_metrics({
            "mae":  mean_absolute_error(valid[TARGET], preds),
            "mape": mean_absolute_percentage_error(valid[TARGET], preds),
        })
        mlflow.set_tag("feature_version", "v1.0")
        mlflow.lightgbm.log_model(model, "model",
            registered_model_name="mdl_aurora_forecast_demanda")
```

## Celda 6 · Promocionar champion

```python
from mlflow.tracking import MlflowClient

client = MlflowClient()
versions = client.search_model_versions("name='mdl_aurora_forecast_demanda'")
best = sorted(versions, key=lambda v: float(client.get_run(v.run_id).data.metrics["mape"]))[0]
client.set_registered_model_alias("mdl_aurora_forecast_demanda", "champion", best.version)
print(f"Champion = v{best.version}")
```
