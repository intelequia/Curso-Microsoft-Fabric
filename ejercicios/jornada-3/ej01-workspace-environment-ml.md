# Ejercicio 1 (Jornada 3) · Workspace y Environment para Aurora ML

**Tiempo estimado:** 30 min · **Modalidad:** fuera de aula

## Objetivo

Preparar el workspace `aurora-ml-dev` con un Environment reproducible que servirá para el resto de ejercicios.

## Requisitos previos

- Workspace `aurora-curso-fabric-<iniciales>` operativo (Jornada 1).
- Lakehouse `lh_aurora` con tablas silver.

## Pasos

1. Crea un nuevo workspace `aurora-ml-dev-<iniciales>` con la misma capacidad.
2. Cambia al workload **Data Science** (app switcher).
3. **+ New → Environment** → `env_aurora_ml`:
   - Runtime: el predeterminado de Spark.
   - **Public libraries** → añade:
     - `prophet`
     - `lightgbm`
     - `mlflow` (ya viene, asegúrate de la versión)
     - `synapseml` (si no preinstalado)
   - **Spark properties**: deja por defecto.
   - Pulsa **Publish** y espera a que el estado sea *Ready* (puede tardar varios minutos).
4. Crea un **shortcut** al Lakehouse `lh_aurora` desde este workspace para no duplicar datos:
   - En `aurora-ml-dev` → **+ New → Lakehouse** → `lh_aurora_ml`.
   - Dentro → **New shortcut → Internal → OneLake** → seleccionar tablas `fact_ventas`, `dim_cliente`, `dim_estacion`, `dim_producto`.
5. Sube los CSVs adicionales del repo a `Files/raw/`:
   - `assets/ml/data/clima_historico.csv`
   - `assets/ml/data/transacciones_fidelizacion.csv`
6. Crea un notebook de prueba `nb_smoke_test`:
   - Adjunta `env_aurora_ml` y `lh_aurora_ml`.
   - Ejecuta:

     ```python
     import lightgbm, prophet, mlflow, synapse.ml
     print("LightGBM:", lightgbm.__version__)
     print("Prophet :", prophet.__version__)
     print("MLflow :", mlflow.__version__)
     df = spark.read.table("fact_ventas")
     print("Filas fact_ventas:", df.count())
     ```

## Entregable

Captura del notebook con la salida de versiones y el `count()`.

## Validación

- ✅ Environment `env_aurora_ml` en estado *Ready*.
- ✅ Lakehouse con shortcuts a las 4 tablas del Lakehouse original.
- ✅ CSVs adicionales en `Files/raw/`.
- ✅ Smoke test ejecuta sin error.
