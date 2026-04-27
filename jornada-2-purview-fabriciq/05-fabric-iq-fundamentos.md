# J2-M5 · Fabric IQ: qué es, arquitectura y posicionamiento

**Duración:** 35 min · **Formato:** explicación + demo en vivo

## Objetivos

1. Entender qué es **Fabric IQ** y por qué Microsoft lo ha lanzado.
2. Conocer su **arquitectura interna** (semantic layer, ontologías, agentes, copilots).
3. Diferenciar **Fabric IQ** de **Copilot in Fabric**, **Power BI Q&A** y **Azure AI Foundry Agents**.
4. Identificar requisitos de tenant y de capacidad para usar Fabric IQ.

## Hilo narrativo

> "Hasta ahora hemos visto el dato y el gobierno. Ahora viene la capa de **inteligencia**: cómo Fabric pone una capa semántica enriquecida con IA encima del dato gobernado, para que **el negocio pueda preguntar en lenguaje natural** sin pasar por un analista, y para que **agentes de IA** razonen sobre datos certificados."

## Contenido

### 1. Qué es Fabric IQ

**Fabric IQ** es la nueva capa de inteligencia que Microsoft introduce en Fabric (anunciada en Ignite 2025, en evolución continua durante 2026). Reúne:

- Una **capa semántica enriquecida y unificada** (ontologías) que va más allá del clásico semantic model de Power BI.
- **Data Agents**: agentes conversacionales razonadores construidos sobre datos del Lakehouse/Warehouse y publicables en Teams, web, Copilot for M365.
- **Copilot for Fabric** integrado en cada experiencia (Notebook, Pipeline, Data Factory, Power BI, KQL).
- **Mejoras del Q&A en lenguaje natural** sobre semantic models.
- **Observabilidad de uso de IA y datos** (qué se pregunta, qué responde, qué dato consume).

> En esencia: convierte el dato gobernado en Fabric en **conocimiento accionable por IA**, con trazabilidad y control.

### 2. Arquitectura conceptual

```
                ┌────────────────────────────────────┐
                │     Aplicaciones / Usuarios        │
                │ Teams · Copilot M365 · Web · API   │
                └────────────────────────────────────┘
                              ▲
                              │
                ┌────────────────────────────────────┐
                │   Data Agents (Fabric IQ)          │
                │  Razonamiento + tools + contexto   │
                └────────────────────────────────────┘
                              ▲
                              │
                ┌────────────────────────────────────┐
                │ Capa semántica unificada (IQ Layer)│
                │  Ontologías · Metrics · Glossary   │
                └────────────────────────────────────┘
                              ▲
                              │
                ┌────────────────────────────────────┐
                │   OneLake (Delta) + Warehouse      │
                │   Eventhouse + Mirrored DB         │
                └────────────────────────────────────┘
                              ▲
                              │
                ┌────────────────────────────────────┐
                │    Microsoft Purview (gobierno)    │
                └────────────────────────────────────┘
```

Tres ideas:

1. **Capa semántica** = el modelo único que entiende qué es "venta", "estación", "cliente activo" y los KPI asociados, por encima del esquema físico.
2. **Data Agents** = agentes con tools (consulta a OneLake, KQL, Warehouse, búsqueda en docs) y memoria, expuestos como API/chat.
3. **Gobierno integrado**: Fabric IQ respeta los permisos, etiquetas y políticas de Purview / RLS / OLS.

### 3. Diferencias con productos previos

| Producto | Qué hace | Diferencia |
| --- | --- | --- |
| **Power BI Q&A** | NL → DAX sobre un semantic model | 1 modelo, 1 conversación, sin razonamiento |
| **Copilot in Fabric** | Asiste al desarrollador (genera SQL, KQL, código Spark, fórmulas DAX) | Foco en productividad del IT |
| **Azure AI Foundry Agents** | Agentes generales sobre Azure (no solo datos Fabric) | Más amplio, pero requiere integrar manualmente con tu data estate |
| **Fabric IQ Data Agents** | Agentes razonadores específicos de tu data estate gobernada en Fabric | Cero plumbing, gobierno automático, multi-modelo |

### 4. Capacidad de razonamiento

Fabric IQ usa modelos avanzados (familia GPT-4o / GPT-5 / razonadores) bajo el capó, con:

- **Function calling / tools**: el agente llama a tools como "execute SQL on Warehouse", "run KQL on Eventhouse", "search OneLake docs".
- **Reasoning loops**: el agente puede planificar varios pasos antes de responder.
- **Memoria conversacional** corta (sesión) y larga (perfil de usuario).
- **Citas y trazabilidad**: cada respuesta incluye los datasets y filas usadas.

### 5. Requisitos

- Capacidad Fabric F-SKU (mínimo recomendado **F4** para experimentación; **F64+** para producción).
- Tenant con **Fabric IQ habilitado** desde el admin portal.
- Modelos LLM aprovisionados por Microsoft en la región de la capacidad (sin coste extra dentro de la capacidad, hasta cuota CU).
- Items origen ya con etiquetas Purview y permisos definidos.

### 6. Tipos de Data Agent

| Tipo | Para quién | Ejemplo Aurora |
| --- | --- | --- |
| **Analytical agent** | Negocio que pregunta KPI | "¿Cómo van las ventas de gasoil este trimestre vs el anterior?" |
| **Operational agent** | Operaciones | "¿Qué surtidores tienen alarmas activas y desde cuándo?" |
| **Search / Knowledge agent** | RR.HH., legal | "Búscame las cláusulas de SLA de los contratos firmados con proveedor X" |
| **Workflow agent** | Procesos automatizados | "Consolida el informe diario de cierre y envíalo al canal Finanzas" |

## Demo en vivo (12 min)

1. Mostrar el área **Fabric IQ** en el portal (workspace o tenant admin).
2. Crear un **Data Agent** vacío llamado `agente-ventas-aurora`.
3. Asociar como fuentes el `wh_aurora` y el modelo semántico `sm_aurora_ventas`.
4. Definir 2–3 instrucciones de sistema (rol, dominio, tono, qué no hacer).
5. Probar preguntas:
   - "¿Cuántas estaciones tenemos por provincia?"
   - "¿Cuál fue el top 5 de productos en marzo?"
   - "Compara las ventas de electricidad vs combustible en el último año."
6. Mostrar la pestaña **Trace** con SQL/DAX generado, citas, y datasets accedidos.
7. Mostrar cómo se publica como **endpoint** y cómo se embebe en Teams.

## Mensajes clave

- "Fabric IQ no es un chatbot — es una capa de razonamiento gobernada sobre tu data estate."
- "Sin gobierno (Purview + sensitivity labels + RLS), el agente expone lo que no debe."
- "El secreto está en la **capa semántica**: si el modelo es bueno, el agente brilla."
