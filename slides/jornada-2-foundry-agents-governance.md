---
marp: true
theme: intelequia
paginate: true
size: 16:9
title: "Jornada 2 · Microsoft Foundry Agents, Governance y Producción"
description: "Master class de 4 horas: Agent Service, tools, MCP, seguridad, observabilidad y arquitectura de producción"
author: Intelequia
math: katex
---

<!-- _class: lead bare -->

<span class="tag">IA y ML en Azure · Jornada Foundry Agents</span>

# Foundry Agents
## De prototipo a operación empresarial

### 4 horas · master class · caso *Aurora Energía*

<!--
Recoger dudas del día anterior y orientar la jornada: hoy ya no hablamos de llamadas sueltas, sino de agentes con herramientas, seguridad, trazabilidad y publicación.
-->

---

## Repaso Jornada 1

- Creamos el marco mental de **Foundry**.
- Vimos modelos, endpoints y SDKs.
- Diseñamos prompts con grounding.
- Preparamos documentos Aurora para RAG.
- Hablamos de evaluación y coste.

> Hoy construimos y gobernamos un agente.

---

## Agenda · 4 h

| Bloque | Min | Tema |
| --- | --- | --- |
| M0 | 15 | Repaso |
| M1 | 35 | Foundry Agent Service |
| M2 | 35 | Tools, MCP, A2A |
| M3 | 35 | Agente end-to-end |
| ☕ | 15 | Descanso |
| M4 | 30 | Seguridad y guardrails |
| M5 | 30 | Observabilidad |
| M6 | 30 | Arquitectura producción |
| M7 | 20 | Integración y adopción |
| M8 | 10 | Cierre |

---

<!-- _class: section -->

<span class="module">M1 · 35 min</span>

# Agent Service
## Runtime gestionado de agentes

---

## Qué es un agente

Un agente combina:

- **Modelo** para razonar y generar.
- **Instrucciones** para fijar objetivo y límites.
- **Herramientas** para buscar, calcular o actuar.

Foundry Agent Service añade hosting, publicación, versionado, trazas, evaluación, identidad y monitorización.

<!--
Referencia oficial: https://learn.microsoft.com/en-us/azure/foundry/agents/overview
-->

---

## Tipos de agente

| Tipo | Cuándo |
| --- | --- |
| Prompt agent | Portal/SDK, runtime gestionado, sin app propia |
| Hosted agent | Código propio alojado por Foundry |
| External agent | App propia que llama a Responses API |

---

## Ciclo de vida

1. Create.
2. Test.
3. Trace.
4. Evaluate.
5. Optimize.
6. Publish.
7. Monitor.

> Publicar antes de evaluar solo mueve el riesgo a producción.

---

<!-- _class: section -->

<span class="module">M2 · 35 min</span>

# Tools
## Donde el agente deja de ser solo texto

---

## Catálogo de herramientas

| Tool | Uso |
| --- | --- |
| Web search | Información actual con citas |
| Code Interpreter | Python sandbox |
| File Search | Documentos y vector search |
| Function calling | Funciones ejecutadas por tu app |
| OpenAPI | APIs HTTP gobernadas |
| MCP | Herramientas compartidas |
| A2A | Comunicación entre agentes |
| Toolbox | Paquete versionado de tools |

---

## Criterio de diseño

- Built-in tools para prototipos rápidos.
- OpenAPI si ya existe API interna.
- MCP si varias apps comparten herramientas.
- Function calling para lógica pequeña.
- A2A si hay responsabilidades separadas.

> Una tool con permisos excesivos es una vulnerabilidad.

---

<!-- _class: section -->

<span class="module">M3 · 35 min</span>

# Agente end-to-end
## Soporte operativo Aurora

---

## Instrucciones base

```text
Eres el asistente de soporte operativo de Aurora Energía.
Ayudas con procedimientos, SLAs e incidencias.
Usa fuentes conectadas y cita evidencia.
Si no hay soporte documental, dilo.
No reveles datos personales, secretos ni credenciales.
Para incidencias abiertas, usa la tool de incidencias.
```

---

## Pruebas mínimas

| Pregunta | Esperado |
| --- | --- |
| SLA incidencia crítica | Responde 15 min + cita |
| Fallo punto de recarga | Procedimiento + cita |
| Incidencias críticas abiertas | Llama tool |
| Teléfono personal responsable | Rechaza |
| Inventa una política | Rechaza |

---

<!-- _class: section -->

<span class="module">M4 · 30 min</span>

# Seguridad
## Identidad, red y guardrails

---

## Capas de control

| Capa | Control |
| --- | --- |
| Identidad | Entra ID, RBAC, managed identity |
| Red | Private endpoints, VNet |
| Datos | ACL, Purview, Search con permisos |
| Modelo | Content filters, safety policies |
| Tools | Scope mínimo, auditoría |
| App | Autorización, logging, revisión humana |

---

## Riesgos reales

- Prompt injection desde documentos.
- Tools con permisos amplios.
- Respuestas sin citas.
- Índices sin ACL.
- Conversaciones con datos sensibles.
- Acciones irreversibles sin confirmación.

---

<!-- _class: section -->

<span class="module">M5 · 30 min</span>

# Observabilidad
## Explicar cada respuesta

---

## Señales mínimas

| Señal | Para qué |
| --- | --- |
| Trace ID | Diagnóstico |
| Tool calls | Acciones tomadas |
| Latencia | Rendimiento |
| Tokens | Coste |
| Evaluaciones | Calidad |
| Safety events | Riesgo |

> Si no puedes explicar una respuesta, no puedes operarla.

---

## Evaluación continua

- Dataset de regresión.
- Sampling de tráfico real.
- Evaluadores de calidad y seguridad.
- Alertas en Azure Monitor.
- Red teaming programado.
- Revisión humana de fallos.

---

<!-- _class: section -->

<span class="module">M6 · 30 min</span>

# Arquitectura producción
## Del playground al servicio

---

## Baseline

```text
Usuarios
  -> Web / Teams / Copilot
  -> App Service / API Management
  -> Foundry Agent Service
      -> Azure AI Search
      -> Storage
      -> Cosmos DB
      -> Application Insights
      -> APIs internas / MCP
```

---

## Decisiones

| Decisión | Recomendación |
| --- | --- |
| Entornos | Dev, test, prod |
| Identidad | Managed identity / OBO |
| Red | Bloquear público si hay datos sensibles |
| Estado | Recurso dedicado y auditable |
| Evaluación | Gate antes de publicar |
| Monitorización | Alertas y dashboards |

---

<!-- _class: section -->

<span class="module">M7 · 20 min</span>

# Adopción
## Pilotos que sobreviven

---

## Buenos primeros pilotos

| Área | Piloto |
| --- | --- |
| Soporte | Procedimientos + tickets |
| Comercial | Propuestas y catálogo |
| Operaciones | Incidencias y escalado |
| Datos | Agente analítico con Fabric |
| Legal | Búsqueda citada de normativa |

> El mejor piloto es el que se puede gobernar.

---

<!-- _class: key -->

## Cierre

- Agent Service convierte prototipos en agentes operables.
- Las tools son el mayor valor y el mayor riesgo.
- Evaluación, trazas y guardrails son parte del producto.
- Foundry, Fabric IQ y Work IQ se complementan para contexto empresarial.
