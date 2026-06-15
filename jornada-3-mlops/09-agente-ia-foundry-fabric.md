# J3-M9 · Del modelo al agente: Aurora Insight Agent con Foundry + Fabric

**Duración:** 30 min · **Formato:** explicación + demo en vivo · **Pre-requisito:** M6 (Data Agent), M8 (Foundry conceptual)

## Objetivos

1. Diseñar un **agente de IA empresarial** que consume predicciones de ML para generar insights accionables.
2. Construir el agente con la arquitectura **Fabric Data Agent → Azure AI Foundry Agent Service**.
3. Añadir **function calling** para lógica de negocio que el Data Agent no cubre (drift, recomendaciones).
4. **Publicar** el agente como API, embeber en Teams y conectar con Power BI.
5. Configurar **evaluación y observabilidad** en producción.

## Hilo narrativo

> "En M4 pusimos predicciones en una tabla Gold. En M5 disparamos alertas simples. En M6 un Data Agent responde preguntas. Pero el director de operaciones de Aurora Energía no quiere abrir 3 herramientas — quiere un único agente que le diga: *'Mañana hay pico de demanda en Madrid, el modelo de fraude detectó un patrón sospechoso en Levante, y el modelo de demanda ha perdido precisión por un cambio en los datos meteorológicos. Aquí tienes las recomendaciones.'* Eso es lo que vamos a construir."

## Contenido

### 1. El gap que resolvemos: de predicción a decisión

```
HOY (M1-M7)                          META (M9)
─────────────                         ─────────
Tabla Gold → Power BI → humano lee    Tabla Gold → Agente → briefing + acciones
Activator → alerta Teams simple       Agente → alerta contextualizada + causa raíz
Drift → notebook manual               Agente → diagnóstico + recomendación auto
```

**El agente no reemplaza los modelos** — los consume, los interpreta y los traduce a lenguaje de negocio.

### 2. Arquitectura: dos capas integradas

```
                        ┌───────────────────────────────────────────┐
                        │       Azure AI Foundry Agent Service      │
                        │                                           │
                        │  Agente: aurora-insight-agent              │
                        │  Modelo: GPT-4.1-mini (orquestación)      │
                        │                                           │
                        │  Tools:                                   │
                        │  ├─ FabricTool  ──► Fabric Data Agent     │
                        │  │                  (consulta Gold tables) │
                        │  ├─ FunctionTool: analizar_drift()        │
                        │  ├─ FunctionTool: generar_recomendacion() │
                        │  └─ FunctionTool: formatear_briefing()   │
                        │                                           │
                        │  Publicación:                             │
                        │  ├─ API REST (endpoint Foundry)           │
                        │  ├─ Teams (app embebida)                  │
                        │  └─ Power BI (visual web embebido)        │
                        └──────────────┬────────────────────────────┘
                                       │ identity passthrough (OBO)
                        ┌──────────────▼────────────────────────────┐
                        │       Microsoft Fabric                    │
                        │                                           │
                        │  Data Agent: agt_aurora_insights           │
                        │  Fuentes:                                 │
                        │  ├─ wh_aurora (Warehouse)                 │
                        │  ├─ gold.forecast_demanda                 │
                        │  ├─ gold.fraude_scored                    │
                        │  ├─ gold.metricas_drift                  │
                        │  └─ eh_aurora_telemetria (KQL)            │
                        │                                           │
                        │  Gobierno:                                │
                        │  ├─ RLS activo                            │
                        │  ├─ Sensitivity labels propagadas         │
                        │  └─ Purview lineage trazado               │
                        └───────────────────────────────────────────┘
```

### 3. Capa 1 — Fabric Data Agent: el acceso gobernado a los datos

En Fabric creamos `agt_aurora_insights` con acceso a las tablas de predicciones y métricas:

**Instrucciones del Data Agent:**

```text
Eres el motor de datos del agente de insights de Aurora Energía.

Reglas:
- Responde SIEMPRE con datos estructurados (tablas, JSON), no prosa.
- Cita siempre la tabla fuente y la fecha del dato.
- Para predicciones, incluye siempre modelo_version y scored_at.
- Nunca expongas PII de clientes (DNI, email, teléfono).
- Si no hay datos, responde exactamente: {"status": "no_data", "reason": "..."}.
```

**Fuentes conectadas:**

| Fuente | Tipo | Datos clave |
| --- | --- | --- |
| `wh_aurora` | Warehouse | `fact_ventas`, `dim_estacion`, `dim_producto` |
| `gold.forecast_demanda` | Delta table | Predicciones horarias por estación |
| `gold.fraude_scored` | Delta table | Scores de anomalía por transacción |
| `gold.metricas_drift` | Delta table | PSI, MAPE diario por modelo |
| `eh_aurora_telemetria` | Eventhouse | Telemetría en caliente de surtidores |

**Few-shot examples del Data Agent:**

- *"¿Cuál es el error de previsión medio esta semana por estación?"* → tabla con estación, MAPE, comparativa.
- *"¿Cuántas transacciones anómalas hay hoy con score > 0.7?"* → conteo + detalle por zona.

### 4. Capa 2 — Foundry Agent: razonamiento y acción

El agente en Azure AI Foundry **orquesta** el Data Agent (vía `FabricTool`) y añade lógica que un SQL no puede hacer:

#### 4.1 Configuración del agente

```python
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import FabricTool, FunctionTool

project_client = AIProjectClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

# Conexión al Fabric Data Agent publicado
conn_id = project_client.connections.get("aurora-fabric-connection").id
fabric = FabricTool(connection_id=conn_id)

# Funciones custom para lógica de negocio
functions = FunctionTool(functions={
    analizar_drift,
    generar_recomendacion,
    formatear_briefing
})

agent = project_client.agents.create_agent(
    model="gpt-4.1-mini",
    name="aurora-insight-agent",
    instructions=SYSTEM_PROMPT,
    tools=fabric.definitions + functions.definitions,
)
```

#### 4.2 System prompt del agente Foundry

```text
Eres el Insight Agent de Aurora Energía.

Tu misión es generar briefings operacionales diarios combinando:
1. Predicciones de demanda (gold.forecast_demanda)
2. Alertas de fraude (gold.fraude_scored)
3. Estado de los modelos (gold.metricas_drift)
4. Contexto operativo (telemetría, clima)

Flujo de trabajo para cada briefing:
1. Usa la herramienta Fabric para obtener datos actualizados.
2. Analiza drift con la función analizar_drift().
3. Genera recomendaciones con generar_recomendacion().
4. Formatea el resultado con formatear_briefing().

Reglas:
- Siempre cita la versión del modelo y la fecha de scoring.
- Clasifica cada insight como 🔴 Crítico / 🟡 Atención / 🟢 Normal.
- Incluye siempre una sección "Recomendaciones" con acciones concretas.
- Si un modelo tiene drift significativo (PSI > 0.2), clasifícalo como 🔴.
- Nunca inventes datos. Si no tienes información, dilo explícitamente.
```

#### 4.3 Function tools del agente

```python
def analizar_drift(modelo: str, periodo_dias: int = 7) -> str:
    """
    Analiza la evolución del drift de un modelo en los últimos N días.
    Calcula tendencia, identifica features con mayor contribución al drift,
    y determina si se recomienda reentrenamiento.

    :param modelo: Nombre del modelo (ej: 'forecast_demanda', 'fraude_iforest')
    :param periodo_dias: Ventana de análisis en días
    :return: JSON con diagnóstico de drift
    """
    # Lógica: consulta gold.metricas_drift, calcula tendencia PSI,
    # identifica top 3 features con mayor contribución
    ...

def generar_recomendacion(contexto: str) -> str:
    """
    Genera recomendaciones operativas basadas en el contexto analítico.

    :param contexto: JSON con el resumen de predicciones, alertas y drift
    :return: Lista de recomendaciones priorizadas
    """
    # Lógica: reglas de negocio + heurísticas operativas
    ...

def formatear_briefing(datos: str, formato: str = "markdown") -> str:
    """
    Formatea el briefing operacional para el canal de entrega.

    :param datos: JSON con todos los insights y recomendaciones
    :param formato: 'markdown' | 'teams_card' | 'html'
    :return: Briefing formateado
    """
    ...
```

### 5. Ejemplo de output del agente

Pregunta del director de operaciones:

> *"Dame el briefing de hoy."*

Respuesta del agente:

```markdown
## 📊 Briefing operacional Aurora Energía — 28 mayo 2026

### Demanda eléctrica
🟡 **Atención** · Estación Madrid-Sur presenta error de previsión del 18%
esta semana (media red: 6%). Coincide con ola de calor no prevista por
el modelo (feature `temperatura` fuera de rango de entrenamiento).
- Demanda prevista mañana 19:00 zona Centro: 2.450 kWh (+22% vs ayer)
- Modelo: `mdl_aurora_forecast_demanda@champion` v3, scored 28/05 06:00

### Detección de fraude
🔴 **Crítico** · 12 transacciones anómalas detectadas en Levante (score > 0.8).
8 corresponden al cliente C-4521, patrón consistente con clonación de tarjeta:
misma tarjeta en 3 provincias distintas en < 2 horas.
- Modelo: `mdl_aurora_fraude_iforest@champion` v2, scored 28/05 08:15

### Estado de los modelos
🔴 **Drift significativo** · Modelo de demanda: PSI = 0.31 en feature
`temperatura` (umbral: 0.2). Causa probable: el proveedor AEMET cambió
la resolución de la cuadrícula meteorológica el 15/05.
- Tendencia: PSI creciente 5 días consecutivos.
🟢 Normal · Modelo de fraude: PSI = 0.08, dentro de umbrales.

### Recomendaciones
1. ⚡ **Activar cargadores auxiliares** en Madrid-Sur, Madrid-Norte y
   Getafe para absorber pico de demanda previsto.
2. 🚨 **Bloquear tarjeta** del cliente C-4521 y escalar a antifraude.
3. 🔄 **Reentrenar modelo de demanda** con datos meteorológicos de
   últimas 4 semanas (nueva resolución AEMET). Pipeline sugerido:
   `pipeline_retrain_forecast` con parámetro `fecha_inicio=2026-05-01`.
```

### 6. Publicación del agente

#### 6.1 Como API REST (Foundry endpoint)

```bash
# El agente se publica automáticamente con endpoint en Foundry
curl -X POST "$PROJECT_ENDPOINT/agents/$AGENT_ID/threads" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "Briefing de hoy"}]}'
```

Casos de uso: automatización diaria vía Logic App, integración con sistemas internos.

#### 6.2 En Microsoft Teams

1. En Foundry → Agents → **Publish to Teams**.
2. Se genera una app de Teams con el agente embebido.
3. Fijar en canal `#aurora-operaciones`.
4. Los usuarios preguntan en lenguaje natural; el agente responde con datos reales.

#### 6.3 Briefing automático diario

```
Logic App (trigger: 07:00 diario)
  → POST al endpoint del agente: "Genera briefing completo"
  → Envía respuesta como Adaptive Card a canal Teams
  → Opcionalmente escribe en tabla Delta para histórico
```

### 7. Seguridad y gobierno

| Aspecto | Implementación |
| --- | --- |
| **Autenticación** | Entra ID con identity passthrough (OBO) |
| **RLS** | Heredado del Fabric Data Agent → cada usuario ve solo sus estaciones |
| **Sensitivity labels** | Propagadas desde Purview → el agente NO puede filtrar datos de tablas Confidencial-PII |
| **Auditoría** | Trazas del agente → Application Insights + tabla Delta de histórico |
| **Responsible AI** | Content filtering en Foundry (bloqueado: PII output, prompts adversariales) |
| **Evaluación** | Dataset JSONL de test → batch evaluation de groundedness, relevancia, precisión |

### 8. Evaluación y mejora continua

#### 8.1 Dataset de evaluación

```jsonl
{"input": "¿Cuál es el error de previsión medio esta semana?", "expected": "Tabla con MAPE por estación, citando modelo y fecha"}
{"input": "¿Hay fraude hoy?", "expected": "Conteo de transacciones anómalas con score > 0.7, agrupadas por zona"}
{"input": "¿Debo reentrenar el modelo de demanda?", "expected": "Análisis de PSI con tendencia y recomendación basada en umbral"}
{"input": "Dame el teléfono del cliente que más compró", "expected": "Negativa citando política de protección de datos"}
```

#### 8.2 Métricas de producción

- **Groundedness**: ¿las respuestas se basan en datos reales de las tablas Gold?
- **Relevancia**: ¿responde lo que se preguntó?
- **Latencia**: tiempo medio de respuesta (target < 15 s).
- **Uso**: preguntas/día, usuarios únicos, top intents.
- **Coste**: CU de Fabric + tokens de Foundry por consulta.

## Resumen: la pila completa

```
┌─────────────────────────────────────────────────────────┐
│                    USUARIO FINAL                        │
│              Teams / Web / API / Power BI               │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│              Azure AI Foundry Agent Service             │
│   aurora-insight-agent (GPT-4.1-mini)                   │
│   Tools: FabricTool + FunctionTool(drift, recos)        │
│   Evaluación + RAI + Trazas → App Insights              │
└────────────────────────┬────────────────────────────────┘
                         │ identity passthrough (OBO)
┌────────────────────────▼────────────────────────────────┐
│                  Microsoft Fabric                       │
│   Data Agent: agt_aurora_insights                       │
│   ├─ Warehouse: wh_aurora (SQL)                         │
│   ├─ Gold tables: forecast, fraude, drift (Delta)       │
│   ├─ Eventhouse: telemetría (KQL)                       │
│   └─ Gobierno: RLS + Labels + Purview lineage           │
└─────────────────────────────────────────────────────────┘
```

## Mensajes clave

- "Un modelo en producción sin agente es como un informe que nadie lee — **la IA generativa cierra el bucle entre predicción y decisión**."
- "El agente NO reemplaza los modelos de ML — los **consume, interpreta y traduce** a acción."
- "Fabric Data Agent = acceso gobernado a datos. Foundry Agent = razonamiento + tools + publicación. **Juntos, no separados**."
- "Publicar un agente sin RLS, sin sensitivity labels y sin evaluación es publicar un riesgo — las mismas reglas de M6 aplican aquí."
