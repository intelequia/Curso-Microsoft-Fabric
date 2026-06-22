# AML-M3 · Experimentos, notebooks y MLflow

**Duración:** 35 min · **Formato:** coding demo

## Objetivos

1. Ejecutar un primer experimento desde notebook o job.
2. Registrar parámetros, métricas y artefactos con MLflow.
3. Comparar ejecuciones y decidir qué modelo merece registrarse.

## Hilo narrativo

> "Un modelo sin tracking es una anécdota. Un experimento trazado permite comparar, repetir y justificar decisiones."

## Contenido

Azure ML integra MLflow para registrar ejecuciones, métricas, parámetros, modelos y artefactos. La misma disciplina sirve para notebooks exploratorios, jobs lanzados desde CLI/SDK y pipelines automatizados.

### Qué registrar

| Señal | Ejemplo |
| --- | --- |
| Parámetros | Algoritmo, profundidad máxima, learning rate, features. |
| Métricas | Accuracy, F1, RMSE, MAE, latencia, coste estimado. |
| Artefactos | Gráficas, matriz de confusión, fichero de predicciones. |
| Modelo | Formato MLflow, sklearn, custom o carpeta serializada. |
| Entorno | Dependencias y versión de código usadas en la ejecución. |

### Snippet de referencia

```python
import mlflow
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score

with mlflow.start_run():
    max_depth = 6
    model = RandomForestClassifier(max_depth=max_depth, random_state=42)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    f1 = f1_score(y_test, preds, average="weighted")

    mlflow.log_param("max_depth", max_depth)
    mlflow.log_metric("f1_weighted", f1)
    mlflow.sklearn.log_model(model, "model")
```

## Demo en vivo

1. Abrir un notebook en Azure ML Studio.
2. Cargar datos de incidencias de Aurora.
3. Entrenar un clasificador simple.
4. Registrar parámetros y métricas con MLflow.
5. Comparar dos ejecuciones cambiando un parámetro.
6. Explicar por qué la mejor métrica no siempre implica el mejor modelo para producción.

## Mensajes clave

- MLflow da trazabilidad portable entre notebook, job y pipeline.
- Comparar modelos exige mirar métricas técnicas y restricciones de negocio.
- Las ejecuciones deben guardar suficiente contexto para poder repetirse.
