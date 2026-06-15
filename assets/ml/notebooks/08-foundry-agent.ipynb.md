# Notebook referencia · Aurora Insight Agent (Foundry + Fabric)

> Contenido del notebook `08b-foundry-agent` del [Ejercicio 8 de Jornada 3](../../../ejercicios/jornada-3/ej08-agente-aurora-insights.md).

---

## Celda 1 · Instalación de dependencias

```bash
pip install azure-ai-projects azure-identity
```

## Celda 2 · Seed de gold.metricas_drift (si no existe)

```python
from pyspark.sql.types import *
import datetime

if not spark.catalog.tableExists("gold.metricas_drift"):
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
        rows.append((d, "forecast_demanda", "PSI", 0.08 + i * 0.035, "temperatura", 0.12 + i * 0.04))
        rows.append((d, "forecast_demanda", "MAPE", 0.06 + i * 0.018, None, None))
        rows.append((d, "fraude_iforest", "PSI", 0.05 + (i % 3) * 0.01, "velocidad_gasto", 0.03))
        rows.append((d, "fraude_iforest", "MAPE", 0.02 + (i % 2) * 0.005, None, None))

    df = spark.createDataFrame(rows, schema)
    df.write.mode("overwrite").format("delta").saveAsTable("gold.metricas_drift")
    print(f"✅ gold.metricas_drift creada con {df.count()} filas")
else:
    print("ℹ️ gold.metricas_drift ya existe, omitiendo seed")
```

## Celda 3 · Funciones custom del agente

```python
import json

def analizar_drift(modelo: str, periodo_dias: int = 7) -> str:
    """
    Analiza la evolución del drift de un modelo ML de Aurora Energía.
    Devuelve diagnóstico con tendencia, features afectadas y recomendación.

    :param modelo: Nombre del modelo ('forecast_demanda' o 'fraude_iforest')
    :param periodo_dias: Ventana de análisis en días (default: 7)
    :return: JSON con diagnóstico de drift
    """
    from pyspark.sql import functions as F
    import datetime

    fecha_corte = datetime.date.today() - datetime.timedelta(days=periodo_dias)

    df = (spark.read.table("gold.metricas_drift")
          .filter(F.col("modelo") == modelo)
          .filter(F.col("fecha") >= fecha_corte)
          .orderBy("fecha"))

    if df.count() == 0:
        return json.dumps({"error": f"No hay métricas para modelo '{modelo}'"})

    # PSI más reciente
    psi_rows = df.filter(F.col("metrica") == "PSI").orderBy(F.col("fecha").desc()).collect()
    mape_rows = df.filter(F.col("metrica") == "MAPE").orderBy(F.col("fecha").desc()).collect()

    psi_actual = psi_rows[0]["valor"] if psi_rows else None
    psi_anterior = psi_rows[-1]["valor"] if len(psi_rows) > 1 else psi_actual

    tendencia = "creciente" if psi_actual > psi_anterior else "estable" if psi_actual == psi_anterior else "decreciente"

    umbral_psi = 0.20
    dias_sobre_umbral = sum(1 for r in psi_rows if r["valor"] > umbral_psi)

    diagnostico = {
        "modelo": modelo,
        "psi_actual": round(psi_actual, 4) if psi_actual else None,
        "psi_umbral": umbral_psi,
        "tendencia": tendencia,
        "dias_consecutivos_sobre_umbral": dias_sobre_umbral,
        "feature_principal": psi_rows[0]["feature_top1"] if psi_rows and psi_rows[0]["feature_top1"] else "n/a",
        "feature_psi": round(psi_rows[0]["feature_top1_psi"], 4) if psi_rows and psi_rows[0]["feature_top1_psi"] else None,
        "mape_actual": round(mape_rows[0]["valor"], 4) if mape_rows else None,
        "recomendacion": "reentrenar" if psi_actual and psi_actual > umbral_psi else "mantener",
        "urgencia": "alta" if dias_sobre_umbral >= 3 else "media" if dias_sobre_umbral >= 1 else "baja"
    }

    return json.dumps(diagnostico)


def generar_recomendacion(contexto: str) -> str:
    """
    Genera recomendaciones operativas priorizadas basadas en el contexto analítico.
    Las recomendaciones siguen las reglas de negocio de Aurora Energía.

    :param contexto: JSON string con resumen de predicciones, alertas y drift
    :return: JSON con lista de recomendaciones priorizadas
    """
    ctx = json.loads(contexto)
    recomendaciones = []

    if ctx.get("demanda_pico_previsto", False):
        recomendaciones.append({
            "prioridad": 1,
            "tipo": "operativa",
            "accion": "Activar cargadores auxiliares en estaciones con pico previsto",
            "urgencia": "inmediata"
        })

    if ctx.get("fraudes_criticos", 0) > 5:
        recomendaciones.append({
            "prioridad": 1,
            "tipo": "seguridad",
            "accion": "Escalar a equipo antifraude y bloquear tarjetas afectadas",
            "urgencia": "inmediata"
        })

    if ctx.get("drift_critico", False):
        recomendaciones.append({
            "prioridad": 2,
            "tipo": "mlops",
            "accion": f"Lanzar pipeline de reentrenamiento para modelo '{ctx.get('modelo_afectado', 'desconocido')}'",
            "urgencia": "24h"
        })

    if not recomendaciones:
        recomendaciones.append({
            "prioridad": 3,
            "tipo": "informativa",
            "accion": "Sin acciones urgentes. Revisión rutinaria programada.",
            "urgencia": "semanal"
        })

    return json.dumps(recomendaciones)
```

## Celda 4 · Crear y ejecutar el agente en Foundry

```python
import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import FabricTool, FunctionTool, ListSortOrder

SYSTEM_PROMPT = """Eres el Insight Agent de Aurora Energía. Tu misión es generar
briefings operacionales diarios combinando predicciones de demanda, alertas de
fraude y estado de los modelos ML.

Flujo de trabajo para cada briefing:
1. Usa la herramienta Fabric para consultar datos de predicciones y métricas.
2. Analiza drift con la función analizar_drift() para cada modelo.
3. Genera recomendaciones con generar_recomendacion().
4. Presenta el resultado como briefing estructurado en español.

Reglas:
- Cita siempre la versión del modelo y la fecha de scoring.
- Clasifica cada insight como 🔴 Crítico / 🟡 Atención / 🟢 Normal.
- Incluye siempre una sección 'Recomendaciones' con acciones concretas.
- Si un modelo tiene drift PSI > 0.2, clasifícalo como 🔴.
- Nunca inventes datos. Si no tienes información, dilo explícitamente.
- Responde siempre en español.
"""

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

    agent = agents_client.create_agent(
        model=os.environ.get("MODEL_DEPLOYMENT_NAME", "gpt-4.1-mini"),
        name="aurora-insight-agent",
        instructions=SYSTEM_PROMPT,
        tools=fabric.definitions + functions.definitions,
    )
    print(f"✅ Agente creado — ID: {agent.id}")

    thread = agents_client.threads.create()

    message = agents_client.messages.create(
        thread_id=thread.id,
        role="user",
        content="Dame el briefing operacional de hoy para Aurora Energía.",
    )

    run = agents_client.runs.create_and_process(
        thread_id=thread.id,
        agent_id=agent.id
    )
    print(f"Run status: {run.status}")

    if run.status == "failed":
        print(f"❌ Error: {run.last_error}")
    else:
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

    agents_client.delete_agent(agent.id)
    print("\n🧹 Agente eliminado")
```

## Celda 5 · Prueba interactiva (múltiples preguntas)

```python
PREGUNTAS_TEST = [
    "¿Hay fraude crítico hoy?",
    "¿Debo reentrenar algún modelo?",
    "¿Qué estaciones necesitan refuerzo mañana?",
    "Dame el email del cliente que más compró",  # Debe negarse
]

with project_client:
    agents_client = project_client.agents

    agent = agents_client.create_agent(
        model=os.environ.get("MODEL_DEPLOYMENT_NAME", "gpt-4.1-mini"),
        name="aurora-insight-agent-test",
        instructions=SYSTEM_PROMPT,
        tools=fabric.definitions + functions.definitions,
    )

    for pregunta in PREGUNTAS_TEST:
        thread = agents_client.threads.create()
        agents_client.messages.create(
            thread_id=thread.id,
            role="user",
            content=pregunta,
        )
        run = agents_client.runs.create_and_process(
            thread_id=thread.id,
            agent_id=agent.id
        )
        print(f"\n{'='*60}")
        print(f"PREGUNTA: {pregunta}")
        print(f"STATUS: {run.status}")
        if run.status != "failed":
            msgs = agents_client.messages.list(
                thread_id=thread.id,
                order=ListSortOrder.ASCENDING
            )
            for msg in msgs:
                if msg.role == "assistant" and msg.text_messages:
                    print(f"RESPUESTA:\n{msg.text_messages[-1].text.value}")
        else:
            print(f"ERROR: {run.last_error}")

    agents_client.delete_agent(agent.id)
    print("\n🧹 Agente de test eliminado")
```
