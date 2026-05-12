# J2-M5 · Data agents en Fabric · fundamentos y posicionamiento

**Duración:** 30 min · **Formato:** explicación + demo en vivo

## Objetivos

1. Entender qué es un **Data agent** de Fabric y por qué es la capa conversacional sobre dato gobernado.
2. Situar el Data agent dentro del **workload Fabric IQ (preview)** y de su arquitectura conceptual.
3. Diferenciar **Data agent** de **Copilot in Fabric**, **Power BI Q&A** y **Azure AI Foundry Agents**.
4. Identificar los requisitos reales de tenant y capacidad para construir un Data agent (lo del lab) y, por separado, los del workload Fabric IQ (preview, opcional).

## Hilo narrativo

> "Hasta ahora hemos visto el dato y el gobierno. Ahora vamos a construir la primera **experiencia conversacional** sobre ese dato gobernado. Para ello usaremos los **Data agents** de Fabric, que es la capacidad madura para preguntar en lenguaje natural sobre Lakehouse, Warehouse, semantic models, Eventhouse y documentos en OneLake, con citas y trazabilidad. Los Data agents se inscriben en un workload más amplio llamado **Fabric IQ**, que Microsoft está construyendo en preview y que iremos viendo como visión y roadmap."

## Contenido

### 1a. Qué es un Data agent

Un **Data agent** es una capacidad de Microsoft Fabric que permite construir un asistente conversacional sobre datos gobernados. Razona en varios pasos, llama a herramientas (consultas SQL sobre Warehouse, DAX sobre semantic model, KQL sobre Eventhouse, búsqueda sobre ficheros de OneLake), respeta los permisos y etiquetas heredados de la fuente y devuelve respuestas con citas trazables. Se publica como endpoint y puede consumirse desde aplicaciones, Teams o una web embebida.

- **Multi-fuente** · Warehouse, Lakehouse, Power BI semantic model, Eventhouse, OneLake Files.
- **Multi-paso** · planifica, llama a herramientas, evalúa y responde.
- **Gobernado** · hereda RLS/OLS, sensitivity labels y permisos de cada fuente.
- **Trazable** · cada respuesta cita datasets, queries generadas y filas usadas.
- **Publicable** · endpoint REST, app de Teams, embed web con Entra ID.

> Un Data agent **no es un chatbot**: es una capa de razonamiento sobre dato gobernado, con auditoría.

### 1b. El workload Fabric IQ (preview)

**Fabric IQ (preview)** es un *workload* de Microsoft Fabric que agrupa varias capacidades pensadas para describir y razonar sobre el dato empresarial. Según la documentación pública actual, incluye:

| Capacidad | Para qué sirve | Estado |
| --- | --- | --- |
| **Ontology** | Vocabulario y semántica de negocio sobre el dato físico | Preview |
| **Graph** | Materializa las relaciones de la ontology como grafo | Preview |
| **Plan** | Define planes que combinan datos y acciones | Preview |
| **Data agent** | Asistente conversacional sobre datos | **Disponible** |
| **Operations agent** | Agente para tareas operativas sobre la plataforma | Preview |
| **Power BI semantic model** | Capa semántica tabular tradicional, integrable como fuente | GA |

> En este curso construiremos un **Data agent** end-to-end. El resto del workload se trata como **visión y roadmap**: explicamos qué resuelve y cómo encaja, sin depender de ello para los ejercicios.

> **Disclaimer.** Workload Fabric IQ, Ontology, Graph, Plan y Operations agent están en **preview**. Su disponibilidad depende de tenant, región y configuración. Verificar antes de comprometer en proyecto.

### 2. Arquitectura conceptual

```text
┌────────────────────────────────────────────────┐
│         Aplicaciones / Usuarios                │
│   Teams · Copilot M365 · Web · API REST        │
└────────────────────────────────────────────────┘
                        ▲
┌────────────────────────────────────────────────┐
│              Data agent (Fabric)               │
│   Razonamiento + tools + citas + memoria       │
└────────────────────────────────────────────────┘
                        ▲
        ┌──── fuentes que el agente puede usar ────┐
        ▼                                          ▼
┌──────────────────────────┐    ┌────────────────────────────────┐
│ Power BI semantic model  │    │ Ontology / Graph (preview)     │
│ (GA · capa semántica hoy)│    │ del workload Fabric IQ         │
└──────────────────────────┘    └────────────────────────────────┘
        ▲                                          ▲
        └──────────────── OneLake ─────────────────┘
        Lakehouse · Warehouse · Eventhouse · Files
                        ▲
┌────────────────────────────────────────────────┐
│   Microsoft Purview · gobierno transversal     │
│   labels · lineage · DLP · access policies     │
└────────────────────────────────────────────────┘
```

Tres ideas:

1. **Capa semántica · hoy** = el **Power BI semantic model** (GA) entiende qué es "venta", "estación", "cliente activo". **Mañana** se complementará con **Ontology (preview)** del workload Fabric IQ.
2. **Data agent** = capacidad conversacional con tools (SQL, DAX, KQL, búsqueda) y memoria, expuesto como API/chat.
3. **Gobierno integrado**: el Data agent respeta los permisos, etiquetas y políticas de Purview / RLS / OLS heredados de cada fuente.

### 3. Diferencias con productos previos

| Producto | Qué hace | Diferencia |
| --- | --- | --- |
| **Power BI Q&A** | NL → DAX sobre **un** semantic model | 1 modelo, sin razonamiento multi-paso |
| **Copilot in Fabric** | Asiste al desarrollador (genera SQL, KQL, código Spark, fórmulas DAX) | Foco en productividad del IT |
| **Azure AI Foundry Agents** | Agentes generales sobre Azure (no solo datos Fabric) | Más amplio, pero requiere integrar manualmente con tu data estate |
| **Fabric · Data agent** | Agente razonador sobre datos gobernados de Fabric | Cero plumbing, gobierno heredado, multi-fuente |
| **Fabric IQ workload (preview)** | *Paraguas* con Ontology, Graph, Plan, Operations agent + Data agent | Visión de capa semántica empresarial; capacidades en preview |

### 4. Capacidad de razonamiento del Data agent

El Data agent usa modelos avanzados aprovisionados por Microsoft dentro de la región de la capacidad Fabric, con:

- **Function calling / tools**: el agente llama a tools como "execute SQL on Warehouse", "run KQL on Eventhouse", "search OneLake docs".
- **Reasoning loops**: el agente puede planificar varios pasos antes de responder.
- **Memoria conversacional** corta (sesión) y larga (perfil de usuario).
- **Citas y trazabilidad**: cada respuesta incluye los datasets y filas usadas.

### 5. Requisitos

**Para construir un Data agent (lo que haremos hoy)**

- Capacidad Fabric F-SKU compatible (orientativo: **F4+** para experimentación, **F64+** para producción).
- Workspace con los items origen ya gobernados (sensitivity labels, RLS/OLS, permisos).
- Modelos LLM aprovisionados por Microsoft en la región de la capacidad (consumo dentro de la cuota CU).

**Para explorar el workload Fabric IQ (preview, opcional)**

- Tenant con el workload Fabric IQ habilitado por el admin.
- Disponibilidad de Ontology / Graph / Plan / Operations agent · sujeta a preview y región.

> En este curso usaremos solo el primer bloque. El segundo es informativo.

### 6. Patrones de uso de un Data agent

| Patrón | Para quién | Ejemplo Aurora |
| --- | --- | --- |
| **Analítico** | Negocio que pregunta KPI | "¿Cómo van las ventas de gasoil este trimestre vs el anterior?" |
| **Operativo / tiempo real** | Operaciones (apoyado en Eventhouse) | "¿Qué surtidores tienen alarmas activas y desde cuándo?" |
| **Conocimiento documental** | RR.HH., legal (apoyado en OneLake Files) | "Búscame las cláusulas de SLA de los contratos firmados con el proveedor X" |
| **Asistencia a procesos** | Procesos de negocio | "Resumen del cierre diario en el canal Finanzas" |

> Patrones de uso, no tipos de producto · todos se construyen con la misma capacidad **Data agent**.

## Demo en vivo (12 min)

1. Crear un **Data agent** en el workspace `aurora-curso-fabric` con nombre `agente-ventas-aurora`.
2. Asociar como fuentes el `wh_aurora` y el modelo semántico `sm_aurora_ventas`.
3. Definir 2–3 instrucciones de sistema (rol, dominio, tono, qué no hacer).
4. Probar preguntas:
   - "¿Cuántas estaciones tenemos por provincia?"
   - "¿Cuál fue el top 5 de productos en marzo?"
   - "Compara las ventas de electricidad vs combustible en el último año."
5. Mostrar la pestaña **Trace** con SQL/DAX generado, citas, y datasets accedidos.
6. Mostrar cómo se publica como **endpoint** y cómo se embebe en Teams.

## Mensajes clave

- "Un **Data agent** no es un chatbot — es una capa de razonamiento gobernada sobre tu data estate."
- "Sin gobierno (Purview + sensitivity labels + RLS), el agente expone lo que no debe."
- "La capa semántica importa: hoy = Power BI semantic model (GA); mañana también Ontology (preview) del workload Fabric IQ."
