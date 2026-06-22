# J1-M1 · Qué es Microsoft Foundry

**Duración:** 30 min · **Formato:** explicación + demo corta

## Objetivos

1. Entender Foundry como plataforma para construir, desplegar y operar aplicaciones de IA.
2. Diferenciar Foundry, Azure OpenAI, Azure Machine Learning y Copilot Studio.
3. Identificar las piezas principales: portal, recurso, proyecto, modelos, agentes, herramientas, evaluaciones y monitorización.

## Hilo narrativo

> "Azure OpenAI nos daba modelos. Foundry nos da una plataforma completa: modelos, agentes, herramientas, conocimiento, evaluación, seguridad y operación."

## Contenido

Microsoft Foundry es la superficie de Microsoft para crear aplicaciones y agentes de IA empresarial. Desde el portal se gestionan proyectos, despliegues de modelos, agentes, herramientas, knowledge bases, evaluaciones y observabilidad.

### Componentes principales

| Pieza | Para qué sirve |
| --- | --- |
| **Foundry portal** | Crear proyectos, explorar modelos, construir agentes y revisar monitorización. |
| **Foundry resource** | Recurso Azure que agrupa endpoints y capacidades. |
| **Project** | Unidad de trabajo para modelos, agentes, herramientas, conexiones y evaluaciones. |
| **Model catalog** | Catálogo de modelos de Microsoft, OpenAI, Anthropic, Mistral, Meta, DeepSeek, xAI, Hugging Face y otros. |
| **Agent Service** | Plataforma gestionada para crear, probar, publicar y monitorizar agentes. |
| **Foundry IQ** | Capa de conocimiento gestionada para conectar datos empresariales a agentes. |
| **Control plane** | Seguridad, tracing, evaluación, red teaming, monitorización y gobierno. |

### Foundry vs Azure OpenAI

- **Azure OpenAI**: endpoint especializado para modelos OpenAI y compatibilidad máxima con la API OpenAI.
- **Foundry**: plataforma multi-modelo y multi-agente con herramientas, proyectos, evaluaciones y operación.

Regla práctica: si solo necesitas llamadas directas a GPT, Azure OpenAI puede ser suficiente. Si necesitas agentes, herramientas, evaluación, catálogo multi-modelo o gobierno de ciclo de vida, Foundry es el punto de entrada.

## Demo en vivo

1. Abrir `https://ai.azure.com`.
2. Cambiar a la experiencia nueva de Foundry.
3. Mostrar un proyecto y su endpoint.
4. Navegar por Model catalog, Agents, Knowledge, Evaluations y Monitoring.
5. Localizar dónde se crean conexiones y herramientas.

## Mensajes clave

- Foundry no es solo un playground: es una plataforma de ciclo de vida.
- El proyecto es la unidad práctica para organizar modelos, agentes y evaluaciones.
- Para nuevos desarrollos, priorizamos Foundry Agent Service y Agent Framework; Prompt Flow queda como legacy.
