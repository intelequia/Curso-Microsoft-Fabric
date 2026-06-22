---
marp: true
theme: intelequia
paginate: true
size: 16:9
title: "Jornada 1 · Microsoft Foundry Core"
description: "Master class de 4 horas: fundamentos, modelos, SDKs, Responses API, RAG, Foundry IQ, evaluación y costes"
author: Intelequia
math: katex
---

<!-- _class: lead bare -->

<span class="tag">IA y ML en Azure · Jornada Foundry Core</span>

# Microsoft Foundry
## Plataforma para construir IA empresarial

### 4 horas · master class · caso *Aurora Energía*

<!--
Presentar el objetivo: pasar de llamadas sueltas a modelos a una plataforma completa de IA con proyectos, modelos, agentes, conocimiento y evaluación. El caso Aurora Energía se usará durante todo el curso.
-->

---

## Qué nos llevaremos hoy

- Entender **qué es Foundry** y cuándo usarlo frente a Azure OpenAI directo.
- Explorar el **catálogo de modelos** y criterios de selección.
- Hacer una primera llamada con **SDK / Responses API**.
- Diseñar prompts con **grounding** y patrón RAG.
- Crear una **knowledge base** con Foundry IQ.
- Ejecutar una primera **evaluación** de calidad y seguridad.

> Hilo conductor: asistente interno de operaciones para **Aurora Energía**.

---

## Agenda · 4 h

| Bloque | Min | Tema |
| --- | --- | --- |
| M0 | 15 | Bienvenida y caso |
| M1 | 30 | Qué es Microsoft Foundry |
| M2 | 35 | Model catalog, despliegues, endpoints y ML |
| M3 | 40 | SDKs y Responses API |
| ☕ | 15 | Descanso |
| M4 | 35 | Prompting, grounding y RAG |
| M5 | 30 | Foundry IQ y knowledge bases |
| M6 | 25 | Evaluación básica |
| M7 | 20 | Costes, límites y modelos |
| M8 | 10 | Cierre |

---

<!-- _class: section -->

<span class="module">M1 · 30 min</span>

# Qué es Foundry
## De modelos a plataforma

---

## Foundry en una frase

Microsoft Foundry es la plataforma para **crear, desplegar, evaluar y operar** aplicaciones y agentes de IA sobre Azure.

| Pieza | Para qué sirve |
| --- | --- |
| Portal | Proyectos, modelos, agentes, evaluaciones |
| Model catalog | Más de un proveedor y familia de modelos |
| Agent Service | Runtime gestionado de agentes |
| Foundry IQ | Conocimiento empresarial para agentes |
| Control plane | Seguridad, evaluación, tracing, monitorización |

<!--
Referencia oficial: https://learn.microsoft.com/en-us/azure/foundry/what-is-foundry
-->

---

## Foundry vs Azure OpenAI

| Si necesitas... | Empieza por... |
| --- | --- |
| Solo llamadas GPT compatibles con OpenAI | Azure OpenAI endpoint |
| Multi-modelo y catálogo amplio | Foundry |
| Agentes con tools y publicación | Foundry Agent Service |
| Evaluación, tracing y monitorización | Foundry |
| Knowledge bases gestionadas | Foundry IQ + Azure AI Search |

> Foundry no sustituye Azure OpenAI: lo amplía como plataforma.

---

<!-- _class: key -->

## Ideas clave

- **Proyecto** = unidad práctica de trabajo.
- **Modelo** = capacidad de razonamiento o generación.
- **Agente** = modelo + instrucciones + herramientas.
- **Operación** = evaluación, trazas, seguridad y coste.

---

<!-- _class: section -->

<span class="module">M2 · 35 min</span>

# Modelos y endpoints
## Elegir con criterio

---

## Familias de modelos

| Familia | Encaje |
| --- | --- |
| GPT-5 / GPT-4.1 | Razonamiento, multimodalidad, tareas complejas |
| GPT mini / nano | Bajo coste, baja latencia, alto volumen |
| Claude | Código, contexto largo, razonamiento |
| Mistral | Multilingüe y propósito general |
| Phi | Modelos pequeños y eficientes |
| Llama / abiertos | Control, personalización, open-weight |

> El mejor modelo es el que cumple calidad, latencia, coste y cumplimiento.

---

## Endpoints que no conviene mezclar

```text
https://<resource>.services.ai.azure.com/api/projects/<project>
```

Foundry SDK, Agent Service, tools, proyecto.

```text
https://<resource>.openai.azure.com/openai/v1
```

Compatibilidad OpenAI para modelos OpenAI desplegados.

---

## Coste real

- Tokens de entrada y salida.
- Embeddings e indexación.
- Azure AI Search.
- Evaluaciones y red teaming.
- Application Insights / Log Analytics.
- Storage, Cosmos DB y red privada.

> Un piloto sin límite de consumo no es un piloto controlado.

---

## ML en Foundry · solo contexto

Foundry también cubre escenarios de **model builders**:

- Modelos abiertos o custom con **managed compute**.
- Infraestructura de Azure Machine Learning para ciertos despliegues.
- Entrenamiento, jobs, pipelines, MLflow y MLOps existen, pero quedan fuera.

> En este curso lo tocamos por encima: el foco es IA generativa, RAG y agentes.

---

<!-- _class: section -->

<span class="module">M3 · 40 min</span>

# Primera app
## SDKs y Responses API

---

## Qué SDK uso

| SDK/API | Uso recomendado |
| --- | --- |
| Foundry SDK | Proyecto, agentes, tools, evaluaciones |
| OpenAI SDK | Compatibilidad con `/openai/v1` |
| Agent Framework | Agentes code-first y multi-agente |
| REST | Integraciones ligeras y automatización |

> Para empresa, autenticación con **Microsoft Entra ID** por defecto.

---

## Primera llamada

```python
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import AzureOpenAI

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(),
    "https://cognitiveservices.azure.com/.default"
)

client = AzureOpenAI(
    azure_endpoint=endpoint,
    azure_ad_token_provider=token_provider,
    api_version="preview"
)

response = client.responses.create(
    model=deployment,
    input="Resume que aporta Microsoft Foundry."
)
```

---

<!-- _class: section -->

<span class="module">M4 · 35 min</span>

# Prompting y RAG
## La respuesta necesita evidencia

---

## Prompt empresarial

```text
Eres el asistente de operaciones de Aurora Energía.
Responde en español, con tono profesional.
Usa solo fuentes conectadas.
Si no hay evidencia suficiente, dilo.
Cita documentos o registros usados.
No reveles datos personales ni secretos.
```

> Un prompt es una especificación operativa, no una frase creativa.

---

## Patrones RAG

| Patrón | Cuándo |
| --- | --- |
| RAG simple | FAQs y documentación estable |
| RAG con metadatos | País, área, versión, permiso |
| RAG evaluado | Calidad y regresiones |
| Agentic retrieval | Varias búsquedas o fuentes |

---

<!-- _class: section -->

<span class="module">M5 · 30 min</span>

# Foundry IQ
## Knowledge bases reutilizables

---

## Foundry IQ en el mapa

| Capa | Enfoque |
| --- | --- |
| Foundry IQ | Conocimiento empresarial para agentes |
| Fabric IQ | Semántica sobre datos analíticos en Fabric |
| Work IQ | Contexto de colaboración de Microsoft 365 |

Flujo:

1. Conectar Azure AI Search.
2. Activar identidad si el origen es OneLake.
3. Dar permisos a Search y Foundry.
4. Añadir fuentes.
5. Configurar retrieval.
6. Probar, conectar a agente y evaluar.

---

## OneLake necesita identidad

```text
Foundry knowledge base
  -> Azure AI Search
  -> managed identity
  -> Fabric OneLake
```

- Search indexa los datos.
- OneLake autoriza a la identidad de Search.
- Foundry necesita acceso a Search/knowledge base.
- No basta con que el usuario tenga permisos en Fabric.

---

<!-- _class: section -->

<span class="module">M6 · 25 min</span>

# Evaluación
## Medir antes de publicar

---

## Métricas iniciales

| Métrica | Pregunta |
| --- | --- |
| Groundedness | ¿Está fundamentada? |
| Relevance | ¿Responde a lo pedido? |
| Coherence | ¿Es consistente? |
| Safety | ¿Evita contenido inseguro? |
| Tool accuracy | ¿Usa la herramienta correcta? |

> Tres pruebas manuales no son evaluación.

---

<!-- _class: section -->

<span class="module">M7 · 20 min</span>

# Producción empieza hoy
## Coste, límites, región

---

## Checklist de decisión

- Calidad mínima.
- Latencia máxima.
- Volumen de tokens.
- Región y residencia.
- Compatibilidad de tools.
- Cuotas TPM/RPM.
- Evaluación y monitorización.

---

<!-- _class: key -->

## Cierre Jornada 1

- Foundry organiza el ciclo completo de IA empresarial.
- El modelo es solo una pieza.
- RAG sin evaluación sigue siendo frágil.
- Mañana convertimos esto en **agentes publicables y gobernados**.
