# J3-M7 · Monitorización, drift y reentrenamiento

**Duración:** 25 min · **Formato:** demo + discusión · **Pre-requisito:** modelo en producción con scoring batch operativo (M4)

## Objetivos

1. Distinguir **data drift**, **concept drift** y **degradación de servicio**.
2. Implementar métricas de drift en notebooks Fabric con **PSI** y **KS test**.
3. Visualizar la salud del modelo en un dashboard Power BI dedicado.
4. Disparar **reentrenamiento automático** vía Pipeline + Deployment Pipelines (Dev → Test → Prod).

## Hilo narrativo

> "El día que el modelo entra en producción, el reloj empieza a correr. El mundo cambia, los datos cambian, la verdad cambia. Sin monitorización, **un modelo en producción es deuda técnica con apariencia de innovación**."

## Contenido

### 1. Tres cosas distintas que llamamos *drift*

| Tipo | Qué cambia | Cómo se detecta |
| --- | --- | --- |
| **Data drift** | Distribución de features de entrada | PSI, KS, χ² entre training y producción |
| **Concept drift** | Relación X → y (el target ya no se comporta igual) | Caída de MAPE / AUC sobre etiquetas frescas |
| **Service drift** | Latencia, errores, valores fuera de rango | Logs del pipeline y de la API |

### 2. PSI sobre features (notebook programado)

```python
import numpy as np

def psi(expected, actual, buckets=10):
    breakpoints = np.quantile(expected, np.linspace(0, 1, buckets + 1))
    breakpoints[0], breakpoints[-1] = -np.inf, np.inf
    e_counts, _ = np.histogram(expected, breakpoints)
    a_counts, _ = np.histogram(actual,   breakpoints)
    e_perc = np.clip(e_counts / e_counts.sum(), 1e-6, None)
    a_perc = np.clip(a_counts / a_counts.sum(), 1e-6, None)
    return float(((a_perc - e_perc) * np.log(a_perc / e_perc)).sum())
```

Convención de interpretación:

- `PSI < 0.1` → sin drift.
- `0.1 ≤ PSI < 0.25` → drift moderado, vigilar.
- `PSI ≥ 0.25` → drift significativo, reentrenar.

### 3. Métrica de negocio: MAPE rolling

- Sobre `gold.forecast_demanda` y `gold.demanda_real` (cuando llega el real) calculamos MAPE diario, semanal y mensual.
- Visualizado en un reporte Power BI **`Salud del modelo Aurora`** con:
  - Tendencia MAPE últimos 90 días.
  - PSI por feature top-10 (heatmap).
  - % de predicciones generadas por cada versión del modelo (`champion` vs. `challenger`).

### 4. Trigger de reentrenamiento

Pipeline `pl_reentrenamiento_forecast`:

1. **Notebook** de monitorización: calcula PSI y MAPE, escribe a tabla `gold.model_health`.
2. **If activity**: si `PSI > 0.25` **o** `MAPE_7d > umbral`, continúa; si no, termina.
3. **Notebook** de feature engineering (M2) con ventana extendida.
4. **Notebook** de training (M3) que registra el modelo como nueva versión con alias `challenger`.
5. **Notebook** de evaluación A/B: scorer ambos contra los últimos 7 días con `y` real y compara.
6. **If activity**: si challenger gana, llamar al **Deployment Pipeline** para promover a `champion`.
7. **Teams notification** con el veredicto.

> Programación: ejecución semanal + ejecución *ad-hoc* desde Activator si el MAPE diario supera 2× el del histórico.

### 5. Deployment Pipelines entre workspaces

- Tres workspaces: `aurora-ml-dev`, `aurora-ml-test`, `aurora-ml-prod`.
- Un **Deployment Pipeline** propaga: notebooks, environments, modelos, pipelines.
- Reglas de **parámetros por entorno**: connection strings, nombres de tablas, alias de modelo.
- **Aprobación** obligatoria al promover a `prod` (M6).

### 6. Anti-patrones

- ❌ Reentrenar cada noche "por si acaso" (consumo de capacidad sin retorno).
- ❌ Reemplazar el champion automáticamente sin shadow.
- ❌ Medir sólo precisión técnica y no impacto de negocio.
- ❌ Monitorizar features pero no la **predicción** (`y_hat`) ni el **target real**.

## Demo en vivo (8 min)

1. Ejecutar `07-drift-monitor` y mostrar la tabla `gold.model_health`.
2. Forzar drift inyectando ruido sobre `temperatura` y ver cómo PSI sube por encima de 0.25.
3. Lanzar manualmente `pl_reentrenamiento_forecast` y seguirlo en runs.
4. Mostrar el Deployment Pipeline con la promoción pendiente de aprobación.

## Mensajes clave

- "**Lo que no se mide, no se opera.** Monitorización es parte del producto, no opcional."
- "Reentrenar **a evidencia**, no a calendario."
- "Deployment Pipelines hacen el camino Dev→Test→Prod **reversible y auditable**."
