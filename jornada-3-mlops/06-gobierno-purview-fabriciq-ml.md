# J3-M6 · Gobierno de ML con Purview y Fabric IQ

**Duración:** 25 min · **Formato:** explicación + demo · **Pre-requisito:** Jornada 2 completada (Purview escaneando el tenant Fabric, Data Agent operativo)

## Objetivos

1. Visualizar el **linaje extremo a extremo**: tabla origen → feature table → experimento → modelo → predicción → reporte.
2. Aplicar **etiquetas de sensibilidad** heredadas a artefactos de ML.
3. Definir **políticas DLP** sobre features que contienen PII.
4. Usar un **Data Agent de Fabric IQ** para responder preguntas de negocio sobre las predicciones.

## Hilo narrativo

> "Llevamos un modelo a producción. Pero auditoría pregunta: ¿qué datos se usaron para entrenarlo? ¿Hay PII? ¿Quién aprobó la promoción a producción? ¿Cuál es la versión que generó esta predicción concreta? Si no podemos responder, **el modelo no debería estar en producción**."

## Contenido

### 1. Linaje en Purview con artefactos Fabric

Cuando Purview escanea el tenant Fabric, captura:

- **Lakehouse tables** y sus columnas.
- **Notebooks** (con las tablas leídas y escritas).
- **Pipelines** y dependencias entre actividades.
- **ML Experiments** y **ML Models** (con el dataset registrado vía `mlflow.log_input`).
- **Semantic Models** y reportes Power BI.

Esto permite ver en el grafo:

```
dim_cliente ─┐
fact_ventas ─┼─► features_demanda_horaria ─► exp_aurora_forecast ─► mdl_aurora_forecast_demanda@champion
clima_hist ──┘                                                                 │
                                                                               ▼
                                                                  gold.forecast_demanda ─► sm_aurora_ventas ─► Reporte "Demanda 48h"
```

### 2. Etiquetas de sensibilidad heredadas

- `dim_cliente` está etiquetado **Confidencial — PII** en Jornada 2.
- Cuando se genera `features_cliente_fraude`, Purview propaga la etiqueta a:
  - La tabla de features.
  - El experimento que la consume.
  - El modelo registrado.
  - El reporte Power BI que muestra la predicción.
- **Sin acción manual.**

### 3. DLP sobre features con PII

Política Purview ejemplo:

> *"Si una tabla Delta tiene etiqueta Confidencial-PII y reside en un workspace Fabric, bloquear la descarga vía OneLake API por usuarios externos al grupo `aurora-data-science`."*

Adicional: alerta cuando un notebook intenta escribir una columna detectada como DNI/IBAN fuera de su tabla original.

### 4. Aprobación de promoción a producción

Patrón recomendado:

1. El modelo se registra en el workspace **dev** con alias `challenger`.
2. Un **Deployment Pipeline** (ver M7) propone la promoción a **test** y **prod**.
3. Antes de promover, se exige:
   - ✅ Métrica MAPE < umbral acordado.
   - ✅ Evaluación de bias / fairness ejecutada (notebook `responsible_ai`).
   - ✅ Etiqueta de sensibilidad asignada.
   - ✅ Aprobación humana de un owner del data product.
4. La promoción queda registrada en el log de auditoría de Fabric y vinculada al ticket de cambio.

### 5. Fabric IQ Data Agent que explica predicciones

Sobre el workspace de ML creamos un Data Agent `agt_aurora_forecast` con:

- **Fuente**: `gold.forecast_demanda` y `gold.demanda_real`.
- **Glosario**: "demanda", "previsión", "error", "estación", "hora pico".
- **Instrucciones**: cita siempre `modelo_version` y `scored_at` en las respuestas.

Preguntas típicas de negocio:

- *"¿Cuál es la demanda prevista para mañana 19:00 en las estaciones de Madrid?"*
- *"¿En qué estaciones el modelo se equivoca más esta semana?"*
- *"¿Qué versión del modelo está generando las predicciones actuales?"*

> El agente **no inventa**: si la pregunta requiere una métrica que no existe en la tabla, lo dice. Y siempre devuelve la query KQL/SQL que ejecutó (cuando el tenant lo permite).

### 6. Responsible AI checklist mínimo

- [ ] Documento de **model card** (tarjeta de modelo) por modelo en producción.
- [ ] Métrica de **fairness** por grupo sensible (provincia, segmento) reportada.
- [ ] **Plan de retirada**: bajo qué condiciones se desactiva el modelo.
- [ ] **Owner** humano identificable (no "el equipo").

## Demo en vivo (8 min)

1. Abrir Purview → buscar `mdl_aurora_forecast_demanda` → vista de **Lineage**.
2. Subir el grafo desde el modelo hasta `clima_historico.csv` y bajar hasta el reporte Power BI.
3. Mostrar la etiqueta de sensibilidad heredada.
4. En el Data Agent, preguntar: *"¿Qué estaciones tienen mayor error de previsión hoy?"*

## Mensajes clave

- "Un modelo **sin linaje no es auditable**, y sin auditabilidad **no es productivo**."
- "La etiqueta de sensibilidad **viaja** desde la columna fuente hasta el reporte final."
- "Fabric IQ no sustituye a Power BI — **lo complementa** para preguntas conversacionales con citas verificables."
