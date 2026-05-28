# Ejercicio 4 (Jornada 3) · Pipeline de scoring batch y visualización

**Tiempo estimado:** 45 min · **Modalidad:** fuera de aula

## Objetivo

Orquestar la inferencia diaria del modelo champion y publicar resultados en Power BI Direct Lake.

## Requisitos previos

- Modelo `mdl_aurora_forecast_demanda@champion` registrado (ejercicio 3).
- Tabla `features_demanda_horaria` operativa (ejercicio 2).

## Pasos

1. Crea el notebook `04-scoring-forecast`:
   - Genera features para las próximas 48 h (usa `clima_pronostico` simulado: copia el clima histórico desplazado).
   - Carga el modelo: `mlflow.pyfunc.load_model("models:/mdl_aurora_forecast_demanda@champion")`.
   - Genera predicciones y escribe `gold.forecast_demanda` con columnas `estacion_id`, `ts_hora`, `kwh_pred`, `modelo_version`, `scored_at`.
   - Usa `mode("overwrite").option("replaceWhere", "ts_hora >= current_date()")`.
2. Crea un **Data Pipeline** `pl_forecast_demanda_diario`:
   - Actividad 1: Notebook de refresco de features (versión incremental del EJ2).
   - Actividad 2: Notebook `04-scoring-forecast`.
   - Actividad 3: **Teams notification** con número de filas predichas.
   - Schedule: diario 06:00.
3. Añade `gold.forecast_demanda` al modelo semántico `sm_aurora_ventas` (de Jornada 1).
4. En Power BI:
   - Crea medidas `Demanda real (kWh)`, `Demanda prevista (kWh)`, `Error % MAPE`.
   - Crea un visual de línea con real vs. previsto agrupado por estación.

## Entregable

- Pipeline ejecutado al menos 1 vez con éxito.
- Captura del visual en Power BI con datos reales y predichos.

## Validación

- ✅ `gold.forecast_demanda` con datos del día actual y siguiente.
- ✅ Columna `modelo_version` con un valor distinto de NULL.
- ✅ Pipeline programado (no sólo manual).
- ✅ Visual publicado en el workspace.
