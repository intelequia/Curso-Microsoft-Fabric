# J1-M3 · Ingesta: Dataflow Gen2 y Data Pipelines

**Duración:** 40 min · **Formato:** explicación + demo en vivo + ejercicio corto

## Objetivos

1. Conocer las **opciones de ingesta** disponibles en Fabric (Dataflow Gen2, Data Pipeline, Copy Job, Eventstream, Mirroring).
2. Construir un **Dataflow Gen2** que aterrice CSV en el Lakehouse.
3. Construir un **Data Pipeline** que orqueste el Dataflow + actividades adicionales.
4. Comprender cuándo usar cada opción.

## Contenido

### 1. Opciones de ingesta en Fabric

| Opción | Cuándo encaja | Lenguaje |
| --- | --- | --- |
| **Dataflow Gen2** | Ingesta + transformación con Power Query, low-code, batch | M / sin código |
| **Data Pipeline** | Orquestación, control de flujo, copia masiva, programación | UI / JSON |
| **Copy Job** (GA reciente) | Copia incremental gestionada (CDC + watermark) | UI |
| **Eventstream** | Streaming continuo desde IoT Hub, Event Hubs, Kafka, sample data | UI |
| **Mirroring** | Réplica casi en tiempo real desde Azure SQL DB, Cosmos, Snowflake, etc. | UI |
| **Notebook Spark** | Ingesta programática con `spark.read` | PySpark / Spark SQL |

**Regla práctica**:

- Si el origen está soportado por un conector estándar y la transformación es media → **Dataflow Gen2**.
- Si necesito orquestar varios pasos, dependencias, errores y notificaciones → **Data Pipeline** (que internamente puede invocar el Dataflow).
- Si el origen es operacional y quiero analítica casi en tiempo real → **Mirroring**.
- Si es streaming continuo → **Eventstream → Eventhouse**.
- Si necesito control programático → **Notebook**.

### 2. Dataflow Gen2 al detalle

- Nueva generación del clásico Dataflow de Power BI, ahora multi-destino y con motor mejorado ("Fast Copy").
- UX = **Power Query Online**: panel de consultas, *Applied Steps*, vista previa de datos, vista de esquema, diagrama y editor M.
- Destinos soportados: Lakehouse, Warehouse, KQL DB, Azure SQL DB, Azure Synapse SQL, Azure Data Explorer.
- **Refresco** programable (similar a Power BI). Compatible con identidades de servicio y service principal.
- **Plantillas .pqt** importables/exportables.
- **Fast Copy**: motor optimizado que se activa para conectores y cargas grandes (CSV/Parquet sobre ADLS Gen2, Azure SQL, etc.).

### 3. Data Pipeline al detalle

- Orquestador heredero de Azure Data Factory v2, integrado en Fabric.
- Actividades: Copy data, Dataflow, Notebook, Spark Job Definition, Stored Procedure, Lookup, ForEach, If/Switch, Until, Wait, Set Variable, Web (HTTP), Office365 Outlook, Teams, etc.
- **Eventos** entre actividades: en éxito (verde), en fallo (rojo), en omisión (naranja), al completar (azul).
- **Programación**: cron, eventos (file arrived), manual.
- **Monitoring Hub**: vista cross-workspace de ejecuciones.
- Integración con **Variables, Parameters, Expressions** (idénticas a ADF).

### 4. Patrón habitual: Pipeline llama a Dataflow

```
[Pipeline pl_aurora_ingesta]
  ├── Activity: Dataflow → df_clientes (carga clientes_raw)
  ├── Activity: Dataflow → df_ventas (carga ventas_raw)
  ├── Activity: Notebook → nb_silver_clean (transforma raw → silver)
  ├── Activity: Stored Procedure (Warehouse) → sp_load_dim_cliente
  ├── On success: Activity Office365 → enviar correo OK
  └── On failure: Activity Teams → mensaje al canal de soporte
```

### 5. Mirroring (mención breve)

- Desde el workspace, **+ Nuevo → Mirrored database**.
- Selecciona origen (Azure SQL DB, Cosmos DB, Snowflake, Fabric SQL DB).
- En segundos aparece como base **espejo** sobre OneLake en Delta. Cualquier item Fabric puede leerla.
- Caso típico: Aurora Energía replica su ERP (Azure SQL) sin ETL para análisis.

## Demo en vivo (15 min)

### Parte 1 — Dataflow Gen2

1. Workspace → **+ Nuevo → Dataflow Gen2**, nombre `df_clientes`.
2. **Get data → Text/CSV** → upload `clientes.csv`.
3. Promover primera fila como cabecera, asignar tipos (forzar `id` como número, `fecha_alta` como fecha).
4. Renombrar `Query1` a `clientes_curado`.
5. **Configurar destino** → Lakehouse `lh_aurora`, tabla `clientes`, modo **Replace**.
6. **Publish** → ejecutar manualmente.
7. Ir al Lakehouse y verificar que aparece la tabla `clientes`.

### Parte 2 — Data Pipeline

1. Workspace → **+ Nuevo → Data pipeline**, nombre `pl_aurora_ingesta`.
2. Añadir actividad **Dataflow** y seleccionar `df_clientes`.
3. Añadir actividad **Copy data** que copie `productos.csv` desde el Lakehouse `Files/landing/` a la tabla `productos` del Lakehouse (ejemplo de uso del asistente).
4. Conectar ambas con flecha **Verde** (en éxito).
5. Añadir actividad **Office365 Outlook** que envíe un correo de fin (opcional, puede saltarse en aula).
6. Validar y ejecutar.
7. Abrir **Monitoring Hub** y mostrar la ejecución.

## Ejercicio corto en aula (5 min)

- Cada alumno crea su `df_clientes` con destino `lh_aurora.clientes`.
- Verifica que la tabla aparece y tiene >0 filas.

## Mensajes clave

- "Dataflow para transformar, Pipeline para orquestar."
- "Si tu origen es operacional, no construyas ETL: usa Mirroring."
- "Monitoring Hub es tu amigo: úsalo siempre antes de pedir ayuda."
