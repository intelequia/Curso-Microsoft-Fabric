# Ejercicio 7 (Jornada 3, opcional) · Monitorización de drift y reentrenamiento

**Tiempo estimado:** 60 min · **Modalidad:** fuera de aula · **Dificultad:** avanzado

## Objetivo

Implementar un notebook de monitorización que calcule PSI por feature y dispare reentrenamiento si supera umbrales.

## Requisitos previos

- Ejercicios 2, 3 y 4 completados.

## Pasos

1. Crea notebook `07-drift-monitor` (referencia: [assets/ml/notebooks/07-drift-monitor.ipynb.md](../../assets/ml/notebooks/07-drift-monitor.ipynb.md)).
2. Implementa:
   - Función `psi(expected, actual, buckets=10)` (módulo M7).
   - Cálculo de PSI para las features `lag_24h`, `temperatura`, `avg_24h` entre:
     - **Baseline**: distribución durante el entrenamiento original.
     - **Producción**: últimos 7 días.
   - Cálculo de MAPE rolling 7 días sobre `gold.forecast_demanda` vs. `fact_ventas` real.
3. Escribe los resultados a `gold.model_health` (una fila por día con columnas `feature`, `psi`, `mape_7d`, `evaluado_en`).
4. Crea un **Data Pipeline** `pl_reentrenamiento_forecast`:
   - Actividad 1: ejecutar `07-drift-monitor`.
   - Actividad 2: **If condition** `PSI > 0.25 OR MAPE_7d > 0.15`.
   - Si True: ejecutar notebooks de features + training (EJ2 + EJ3) y registrar nuevo `challenger`.
   - Actividad 3: notebook de A/B test challenger vs. champion sobre últimos 7 días.
   - Actividad 4: si challenger gana, **invocar Deployment Pipeline** (EJ6) para promocionar.
   - Actividad 5: notificación Teams con veredicto.
5. Programa el pipeline semanal (lunes 03:00).
6. **Prueba forzada de drift**: ejecuta un notebook auxiliar que añada ruido `+30%` a la columna `temperatura` durante 3 días sintéticos. Lanza el pipeline manualmente y verifica que se dispara el reentrenamiento.

## Entregable

- Tabla `gold.model_health` con al menos 7 filas.
- Captura del pipeline ejecutado tras el drift forzado, mostrando que entra en la rama True.
- Captura del nuevo `challenger` registrado.

## Validación

- ✅ Notebook calcula PSI correctamente (compara con `scipy.stats.ks_2samp` como contraste).
- ✅ Pipeline condicional ejecuta sólo cuando hay drift.
- ✅ Promoción a champion sólo si A/B lo justifica.
- ✅ Notificación Teams recibida.
