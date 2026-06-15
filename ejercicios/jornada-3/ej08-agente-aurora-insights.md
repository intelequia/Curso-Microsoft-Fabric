# Ejercicio 8 (Jornada 3) · Aurora Insight Agent — Agente de IA con Foundry + Fabric

**Tiempo estimado:** 60 min · **Modalidad:** guiado en aula o fuera de aula

## Objetivo

Construir un agente de IA que consuma las predicciones de los modelos ML desplegados en ejercicios anteriores, genere briefings operacionales en lenguaje natural y se publique integrado en el ecosistema Azure (API + Teams).

## Requisitos previos

- Workspace `aurora-curso-fabric` con:
  - Tabla `gold.forecast_demanda` poblada (EJ3-04).
  - Tabla `gold.fraude_scored` poblada (EJ3-05).
  - Warehouse `wh_aurora` con `fact_ventas`, `dim_estacion`.
- Data Agent `agente-ventas-aurora` de Jornada 2 (EJ2-03) operativo y publicado.
- Acceso a un **proyecto en Azure AI Foundry** con modelo GPT-4.1-mini desplegado.
- Python SDK instalado: `azure-ai-projects`, `azure-identity`.

## Pasos

### Parte A · Preparar la tabla de métricas de drift (10 min)

> Si completaste EJ3-07 (drift), ya tienes `gold.metricas_drift`. Si no, créala con datos simulados.

1. En el workspace, crea el notebook `08a-metricas-drift-seed`.
2. Ejecuta el siguiente código para crear la tabla con datos de ejemplo:

```python
from pyspark.sql import SparkSession
from pyspark.sql.types import *
import datetime

schema = StructType([
    StructField("fecha", DateType()),
    StructField("modelo", StringType()),
    StructField("metrica", StringType()),
    StructField("valor", DoubleType()),
    StructField("feature_top1", StringType()),
    StructField("feature_top1_psi", DoubleType()),
])

rows = []
base = datetime.date(2026, 5, 21)
for i in range(7):
    d = base + datetime.timedelta(days=i)
    # Modelo demanda — drift creciente en temperatura
    rows.append((d, "forecast_demanda", "PSI", 0.08 + i * 0.035, "temperatura", 0.12 + i * 0.04))
    rows.append((d, "forecast_demanda", "MAPE", 0.06 + i * 0.018, None, None))
    # Modelo fraude — estable
    rows.append((d, "fraude_iforest", "PSI", 0.05 + (i % 3) * 0.01, "velocidad_gasto", 0.03))
    rows.append((d, "fraude_iforest", "MAPE", 0.02 + (i % 2) * 0.005, None, None))

df = spark.createDataFrame(rows, schema)
df.write.mode("overwrite").format("delta").saveAsTable("gold.metricas_drift")
print(f"✅ gold.metricas_drift creada con {df.count()} filas")
```

3. Valida: `spark.sql("SELECT * FROM gold.metricas_drift ORDER BY fecha DESC LIMIT 5").show()`

### Parte B · Crear y publicar el Fabric Data Agent (15 min)

1. Workspace → **+ New** → **Data agent**.
2. Nombre: `agt_aurora_insights`.

3. **Instrucciones del agente:**

```text
Eres el motor de datos del sistema de insights operacionales de Aurora Energía.

Reglas:
- Responde siempre con datos estructurados (tablas o JSON), no con texto libre.
- Cita SIEMPRE la tabla origen, la versión del modelo y la fecha de scoring.
- Para predicciones de demanda, incluye estación, hora, valor previsto y valor real si está disponible.
- Para fraude, incluye score de anomalía, cliente (solo ID, nunca PII), zona y timestamp.
- Para drift, incluye PSI, MAPE, feature con mayor contribución y tendencia (creciente/estable/decreciente).
- Si no hay datos para una consulta, responde: {"status": "no_data", "reason": "explicación"}.
- Nunca expongas DNI, email, teléfono ni datos personales de clientes.
```

4. **Conectar fuentes:**

| Fuente | Tipo |
| --- | --- |
| `wh_aurora` | Warehouse (SQL endpoint) |
| `gold.forecast_demanda` | Delta table en Lakehouse |
| `gold.fraude_scored` | Delta table en Lakehouse |
| `gold.metricas_drift` | Delta table en Lakehouse |

5. **Few-shot examples** (añadir al menos 3):

   - **Pregunta:** "¿Cuál es el MAPE medio de la última semana para el modelo de demanda?"
     **Respuesta esperada:** tabla con fecha, MAPE, tendencia.

   - **Pregunta:** "¿Cuántas transacciones con score > 0.7 hay hoy?"
     **Respuesta esperada:** conteo agrupado por zona/estación.

   - **Pregunta:** "¿Qué feature tiene mayor PSI en el modelo de demanda?"
     **Respuesta esperada:** feature name, PSI value, tendencia últimos 7 días.

6. **Probar** el Data Agent con las 3 preguntas. Ajustar instrucciones si las respuestas no son estructuradas.

7. **Publicar** el Data Agent → copiar el `workspace_id` y `artifact_id` del endpoint publicado.

### Parte C · Crear el agente en Azure AI Foundry (25 min)

#### C.1 Configurar la conexión Fabric en Foundry

1. Ir a [ai.azure.com](https://ai.azure.com) → tu proyecto.
2. **Connected resources** → **New connection** → **Microsoft Fabric**.
3. Rellenar:
   - **Connection name**: `aurora-fabric-connection`
   - Custom keys:
     - `workspace-id`: el ID del workspace de Fabric.
     - `artifact-id`: el ID del Data Agent publicado.
   - Marcar **Is Secret**.
4. Guardar la conexión.

#### C.2 Crear el agente con FabricTool + FunctionTool

1. Crear el notebook `08b-foundry-agent` (puede ser local o en Fabric).
2. Instalar dependencias:

```bash
pip install azure-ai-projects azure-identity
```

3. Código del agente:

```python
import os
import json
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import FabricTool, FunctionTool, ListSortOrder

# --- Funciones custom del agente ---

def analizar_drift(modelo: str, periodo_dias: int = 7) -> str:
    """
    Analiza la evolución del drift de un modelo ML de Aurora Energía.
    Devuelve diagnóstico con tendencia, features afectadas y recomendación.

    :param modelo: Nombre del modelo ('forecast_demanda' o 'fraude_iforest')
    :param periodo_dias: Ventana de análisis en días (default: 7)
    :return: JSON con diagnóstico de drift
    """
    # En producción, esto consultaría gold.metricas_drift
    # Aquí simulamos la lógica para el ejercicio
    diagnosticos = {
        "forecast_demanda": {
            "modelo": "forecast_demanda",
            "psi_actual": 0.31,
            "psi_umbral": 0.20,
            "tendencia": "creciente",
            "dias_consecutivos_sobre_umbral": 3,
            "feature_principal": "temperatura",
            "feature_psi": 0.40,
            "causa_probable": "Cambio de resolución en cuadrícula AEMET desde 15/05",
            "recomendacion": "reentrenar",
            "urgencia": "alta"
        },
        "fraude_iforest": {
            "modelo": "fraude_iforest",
            "psi_actual": 0.08,
            "psi_umbral": 0.20,
            "tendencia": "estable",
            "dias_consecutivos_sobre_umbral": 0,
            "feature_principal": "velocidad_gasto",
            "feature_psi": 0.03,
            "causa_probable": None,
            "recomendacion": "mantener",
            "urgencia": "baja"
        }
    }
    return json.dumps(diagnosticos.get(modelo, {"error": "modelo no encontrado"}))


def generar_recomendacion(contexto: str) -> str:
    """
    Genera recomendaciones operativas priorizadas basadas en el contexto analítico.
    Las recomendaciones siguen las reglas de negocio de Aurora Energía.

    :param contexto: JSON string con resumen de predicciones, alertas y drift
    :return: JSON con lista de recomendaciones priorizadas
    """
    ctx = json.loads(contexto)
    recomendaciones = []

    # Regla 1: Pico de demanda → activar recursos
    if ctx.get("demanda_pico_previsto", False):
        recomendaciones.append({
            "prioridad": 1,
            "tipo": "operativa",
            "accion": "Activar cargadores auxiliares en estaciones con pico previsto",
            "urgencia": "inmediata"
        })

    # Regla 2: Fraude detectado → escalar
    if ctx.get("fraudes_criticos", 0) > 5:
        recomendaciones.append({
            "prioridad": 1,
            "tipo": "seguridad",
            "accion": "Escalar a equipo antifraude y bloquear tarjetas afectadas",
            "urgencia": "inmediata"
        })

    # Regla 3: Drift alto → reentrenar
    if ctx.get("drift_critico", False):
        recomendaciones.append({
            "prioridad": 2,
            "tipo": "mlops",
            "accion": "Lanzar pipeline de reentrenamiento con datos recientes",
            "urgencia": "24h"
        })

    return json.dumps(recomendaciones)


# --- Configuración del agente ---

SYSTEM_PROMPT = """Eres el Insight Agent de Aurora Energía. Tu misión es generar
briefings operacionales diarios combinando predicciones de demanda, alertas de
fraude y estado de los modelos ML.

Flujo de trabajo para cada briefing:
1. Usa la herramienta Fabric para consultar datos de predicciones y métricas.
2. Analiza drift con la función analizar_drift() para cada modelo.
3. Genera recomendaciones con generar_recomendacion().
4. Presenta el resultado como briefing estructurado.

Reglas:
- Cita siempre la versión del modelo y la fecha de scoring.
- Clasifica cada insight como 🔴 Crítico / 🟡 Atención / 🟢 Normal.
- Incluye siempre una sección 'Recomendaciones' con acciones concretas.
- Si un modelo tiene drift PSI > 0.2, clasifícalo como 🔴.
- Nunca inventes datos. Si no tienes información, dilo explícitamente.
- Responde siempre en español.
"""

# --- Crear el agente ---

project_client = AIProjectClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

# Fabric Data Agent como tool
conn_id = project_client.connections.get("aurora-fabric-connection").id
fabric = FabricTool(connection_id=conn_id)

# Funciones custom como tools
functions = FunctionTool(functions={analizar_drift, generar_recomendacion})

with project_client:
    agents_client = project_client.agents

    # Crear agente
    agent = agents_client.create_agent(
        model=os.environ.get("MODEL_DEPLOYMENT_NAME", "gpt-4.1-mini"),
        name="aurora-insight-agent",
        instructions=SYSTEM_PROMPT,
        tools=fabric.definitions + functions.definitions,
    )
    print(f"✅ Agente creado — ID: {agent.id}")

    # Crear thread y enviar pregunta
    thread = agents_client.threads.create()

    message = agents_client.messages.create(
        thread_id=thread.id,
        role="user",
        content="Dame el briefing operacional de hoy para Aurora Energía.",
    )

    # Ejecutar el agente (procesa tools automáticamente)
    run = agents_client.runs.create_and_process(
        thread_id=thread.id,
        agent_id=agent.id
    )
    print(f"Run status: {run.status}")

    if run.status == "failed":
        print(f"❌ Error: {run.last_error}")
    else:
        # Leer respuesta
        messages = agents_client.messages.list(
            thread_id=thread.id,
            order=ListSortOrder.ASCENDING
        )
        for msg in messages:
            if msg.role == "assistant" and msg.text_messages:
                print("\n" + "=" * 60)
                print("BRIEFING DEL AGENTE:")
                print("=" * 60)
                print(msg.text_messages[-1].text.value)

    # Limpiar
    agents_client.delete_agent(agent.id)
    print("\n🧹 Agente eliminado")
```

4. Configurar variables de entorno:

```bash
# Endpoint de tu proyecto Foundry (encontrar en Overview del proyecto)
export PROJECT_ENDPOINT="https://tu-proyecto.services.ai.azure.com/api/projects/tu-proyecto"
# Nombre del deployment del modelo
export MODEL_DEPLOYMENT_NAME="gpt-4.1-mini"
```

5. Ejecutar y verificar que el agente:
   - Consulta el Fabric Data Agent para obtener datos.
   - Llama a `analizar_drift()` para cada modelo.
   - Genera recomendaciones contextualizadas.
   - Produce un briefing estructurado en español.

#### C.3 Preguntas adicionales de prueba

Probar el agente con estas preguntas cambiando el `content` del mensaje:

| # | Pregunta | Qué debe hacer el agente |
|---|----------|--------------------------|
| 1 | "¿Hay fraude crítico hoy?" | Consultar Fabric → fraude_scored, contar score > 0.7, dar contexto |
| 2 | "¿Debo reentrenar algún modelo?" | Llamar analizar_drift() para ambos modelos, recomendar |
| 3 | "¿Qué estaciones necesitan refuerzo mañana?" | Consultar forecast_demanda, identificar picos, recomendar acciones |
| 4 | "Dame el email del cliente que más compró" | **Negarse** citando política de PII |

### Parte D · Publicar en Teams (10 min)

> Requiere permisos de administrador del tenant de Teams. Si no los tienes, haz la publicación vía API.

#### Opción 1: Publicación vía portal Foundry

1. En Foundry → Agents → seleccionar `aurora-insight-agent`.
2. Click en **Publish** → **Microsoft Teams**.
3. Seguir el wizard para generar la app de Teams.
4. Instalar la app en el canal `#aurora-operaciones`.
5. Probar enviando: *"Briefing de hoy"* en el chat del agente en Teams.

#### Opción 2: Publicación como API + Logic App

1. Copiar el endpoint REST del agente desde Foundry.
2. Crear una **Logic App** con:
   - Trigger: **Recurrence** → cada día a las 07:00.
   - Action 1: **HTTP** → POST al endpoint del agente con body `{"content": "Briefing diario completo"}`.
   - Action 2: **Post adaptive card** al canal de Teams con la respuesta.
3. Activar y esperar al día siguiente para validar.

## Entregable

- Data Agent `agt_aurora_insights` publicado en Fabric.
- Agente `aurora-insight-agent` funcional en Foundry.
- Captura del briefing generado por el agente.
- (Bonus) Captura de la publicación en Teams o del endpoint API.

## Validación

- ✅ El Data Agent responde con datos estructurados citando tabla y fecha.
- ✅ El agente Foundry combina FabricTool + FunctionTool en una sola respuesta.
- ✅ El briefing incluye los 3 bloques: demanda, fraude, drift.
- ✅ Las recomendaciones son concretas y accionables.
- ✅ El agente se niega a devolver PII cuando se le pide.
- ✅ (Bonus) El agente es accesible desde Teams o vía API REST.

## Arquitectura resultante

```
┌────────────────────────────────────────────────────────┐
│  Usuario (Teams / Web / API)                           │
└────────────────┬───────────────────────────────────────┘
                 │
┌────────────────▼───────────────────────────────────────┐
│  Azure AI Foundry Agent Service                        │
│  aurora-insight-agent (GPT-4.1-mini)                   │
│  ├─ FabricTool → agt_aurora_insights                   │
│  ├─ FunctionTool: analizar_drift()                     │
│  └─ FunctionTool: generar_recomendacion()              │
└────────────────┬───────────────────────────────────────┘
                 │ identity passthrough (OBO)
┌────────────────▼───────────────────────────────────────┐
│  Microsoft Fabric                                      │
│  ├─ wh_aurora (Warehouse)                              │
│  ├─ gold.forecast_demanda (Delta)                      │
│  ├─ gold.fraude_scored (Delta)                         │
│  ├─ gold.metricas_drift (Delta)                        │
│  └─ Gobierno: RLS + Labels + Purview                   │
└────────────────────────────────────────────────────────┘
```

## Para ir más allá (opcional)

- Añadir `eh_aurora_telemetria` (Eventhouse) como fuente del Data Agent para preguntas sobre surtidores.
- Implementar un `formatear_briefing()` que genere Adaptive Cards de Teams directamente.
- Conectar trazas del agente a Application Insights para monitorizar uso y calidad.
- Crear un dataset de evaluación JSONL y lanzar batch evaluation en Foundry.
