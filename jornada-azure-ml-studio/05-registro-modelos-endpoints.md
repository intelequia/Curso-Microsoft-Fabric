# AML-M5 · Registro de modelos, endpoints e inferencia

**Duración:** 35 min · **Formato:** explicación + demo técnica

## Objetivos

1. Registrar un modelo versionado en Azure ML.
2. Diferenciar inferencia online y batch.
3. Entender qué se despliega: modelo, environment, scoring script y configuración.

## Hilo narrativo

> "Entrenar no es entregar. El modelo empieza a ser útil cuando alguien puede consumirlo de forma controlada."

## Contenido

El registro de modelos permite versionar artefactos aprobados para pruebas o producción. Los endpoints gestionados exponen el modelo para consumo online o batch sin tener que construir toda la infraestructura desde cero.

### Tipos de inferencia

| Tipo | Cuándo usarlo |
| --- | --- |
| **Managed online endpoint** | Predicción síncrona, baja latencia, integración con apps o APIs. |
| **Batch endpoint** | Scoring programado, grandes volúmenes, integración con lakehouse o procesos analíticos. |

### Piezas de un despliegue

| Pieza | Función |
| --- | --- |
| **Modelo** | Artefacto registrado y versionado. |
| **Environment** | Dependencias de inferencia. |
| **Scoring script** | Funciones `init()` y `run()` para cargar modelo y predecir. |
| **Deployment** | Asociación de modelo, compute, entorno y configuración. |
| **Endpoint** | URL, autenticación, tráfico y logs. |

### Snippet conceptual de scoring

```python
import json
import mlflow

def init():
    global model
    model = mlflow.pyfunc.load_model("model")

def run(raw_data):
    data = json.loads(raw_data)
    predictions = model.predict(data["records"])
    return {"predictions": predictions.tolist()}
```

## Demo en vivo

1. Seleccionar una ejecución con buen resultado.
2. Registrar el modelo desde Azure ML Studio.
3. Crear un endpoint online de prueba o revisar uno preparado.
4. Enviar una petición de ejemplo.
5. Mostrar alternativa batch para puntuar un fichero en Storage/Fabric.

## Mensajes clave

- El registro separa experimento de artefacto candidato a producción.
- Online endpoint y batch endpoint resuelven problemas distintos.
- La seguridad del endpoint debe diseñarse desde el inicio: identidad, red, logs y control de acceso.
