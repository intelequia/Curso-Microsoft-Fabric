# IA y ML en Azure

Master class modular sobre **Microsoft Foundry** y **Azure Machine Learning Studio**. La guía actual mantiene las jornadas de Foundry y añade una jornada completa de Azure ML Studio, todas con formato explicación + demo, ejercicios cortos en aula y práctica guiada para completar fuera del horario.

> Todos los datos, documentos, nombres de empresa y casos de uso son **ficticios**. El hilo conductor es **Aurora Energía**, un operador inventado con estaciones de servicio, comercializadora eléctrica y soporte interno.

## Objetivos generales

Al finalizar el curso, el alumno será capaz de:

1. Entender qué es **Microsoft Foundry**, dónde encaja respecto a Azure OpenAI y qué aporta como plataforma de desarrollo de IA empresarial.
2. Crear proyectos, desplegar modelos, elegir endpoints y consumir modelos con SDK/API.
3. Construir agentes con **Foundry Agent Service**, instrucciones, herramientas, conocimiento empresarial y trazabilidad.
4. Diseñar una solución RAG con **Foundry IQ** y Azure AI Search, con respuestas citadas y respetando permisos.
5. Usar **Azure Machine Learning Studio** para preparar datos, entrenar modelos, registrar experimentos, desplegar endpoints y operar modelos con MLOps.
6. Relacionar Foundry, Azure ML Studio y Fabric para decidir qué plataforma usar en cada parte de una solución de IA empresarial.

## Agenda

### Jornada 1 - Microsoft Foundry Core (4 h)

| Bloque | Duración | Tema |
| --- | --- | --- |
| J1-M0 | 15 min | Bienvenida, contexto y caso Aurora Energía |
| J1-M1 | 30 min | [Qué es Microsoft Foundry](jornada-1-foundry/01-que-es-foundry.md) |
| J1-M2 | 35 min | [Model catalog, despliegues, endpoints y panorama ML](jornada-1-foundry/02-modelos-despliegues.md) |
| J1-M3 | 40 min | [Primera aplicación con SDKs y Responses API](jornada-1-foundry/03-sdk-responses-api.md) |
| - | 15 min | **Descanso** |
| J1-M4 | 35 min | [Prompting, grounding y patrones RAG](jornada-1-foundry/04-prompting-grounding-rag.md) |
| J1-M5 | 30 min | [Foundry IQ y knowledge bases](jornada-1-foundry/05-foundry-iq-knowledge.md) |
| J1-M6 | 25 min | [Evaluación básica de calidad y seguridad](jornada-1-foundry/06-evaluacion-basica.md) |
| J1-M7 | 20 min | [Costes, límites, regiones y elección de modelo](jornada-1-foundry/07-costes-limites-modelos.md) |
| J1-M8 | 10 min | Cierre, dudas y ejercicios |

### Jornada 2 - Agents, Governance y Producción (4 h)

| Bloque | Duración | Tema |
| --- | --- | --- |
| J2-M0 | 15 min | Repaso de la jornada 1 |
| J2-M1 | 35 min | [Foundry Agent Service y ciclo de vida](jornada-2-foundry-agents-governance/01-agent-service.md) |
| J2-M2 | 35 min | [Herramientas: web, code, file search, functions, MCP, A2A](jornada-2-foundry-agents-governance/02-tools-mcp-a2a.md) |
| J2-M3 | 35 min | [Construir un agente end-to-end](jornada-2-foundry-agents-governance/03-agente-end-to-end.md) |
| - | 15 min | **Descanso** |
| J2-M4 | 30 min | [Seguridad, identidad, red privada y guardrails](jornada-2-foundry-agents-governance/04-seguridad-guardrails.md) |
| J2-M5 | 30 min | [Observabilidad, tracing, evaluación continua y red teaming](jornada-2-foundry-agents-governance/05-observabilidad.md) |
| J2-M6 | 30 min | [Arquitectura de producción](jornada-2-foundry-agents-governance/06-arquitectura-produccion.md) |
| J2-M7 | 20 min | [Integración, adopción y roadmap](jornada-2-foundry-agents-governance/07-integracion-roadmap.md) |
| J2-M8 | 10 min | Cierre y próximos pasos |

### Jornada Azure Machine Learning Studio (4 h)

| Bloque | Duración | Tema |
| --- | --- | --- |
| AML-M0 | 15 min | Bienvenida, mapa Azure AI/ML y caso Aurora Energía |
| AML-M1 | 30 min | [Qué es Azure Machine Learning Studio](jornada-azure-ml-studio/01-que-es-azure-ml-studio.md) |
| AML-M2 | 35 min | [Datos, compute y entornos](jornada-azure-ml-studio/02-datos-compute-entornos.md) |
| AML-M3 | 35 min | [Experimentos, notebooks y MLflow](jornada-azure-ml-studio/03-experimentos-notebooks-mlflow.md) |
| - | 15 min | **Descanso** |
| AML-M4 | 35 min | [AutoML, Designer y pipelines](jornada-azure-ml-studio/04-automl-designer-pipelines.md) |
| AML-M5 | 35 min | [Registro de modelos, endpoints e inferencia](jornada-azure-ml-studio/05-registro-modelos-endpoints.md) |
| AML-M6 | 30 min | [MLOps, gobierno y monitorización](jornada-azure-ml-studio/06-mlops-gobierno-monitorizacion.md) |
| AML-M7 | 20 min | [Integración con Foundry y Fabric](jornada-azure-ml-studio/07-integracion-foundry-fabric.md) |
| AML-M8 | 10 min | Cierre y próximos pasos |

## Estructura de este repositorio

```text
contenidos/
├── README.md
├── 00-preparacion-entorno.md
├── 00-preparacion-demo-formador.md
├── requisitos.md
├── jornada-1-foundry/
├── jornada-2-foundry-agents-governance/
├── jornada-azure-ml-studio/
├── ejercicios/
│   ├── jornada-1/
│   ├── jornada-2/
│   └── azure-ml-studio/
├── assets/
│   ├── data/
│   ├── docs/
│   └── code/
├── slides/
└── recursos.md
```

## Metodología

- **Master class** con explicación, demo en vivo y conversación técnica.
- **2 ejercicios cortos por jornada** para fijar conceptos.
- **Ejercicios para casa** con checklist de validación.
- **Caso unificado**: todos los módulos giran alrededor del asistente de operaciones de Aurora Energía.
- **Enfoque actual**: se usa la experiencia nueva de Foundry. Prompt Flow se menciona solo como tecnología legacy en retirada.
- **Separación de plataformas**: Foundry para aplicaciones generativas y agentes; Azure ML Studio para entrenamiento, registro, despliegue y operación de modelos ML; Fabric como capa de datos y analítica ya cubierta en el itinerario.

## Antes de empezar

1. Lee [requisitos.md](requisitos.md).
2. Sigue [00-preparacion-entorno.md](00-preparacion-entorno.md) para preparar Azure, Foundry, Azure ML Studio y las herramientas locales.
3. Revisa los documentos de [assets/docs](assets/docs) y los datos de [assets/data](assets/data), que se usan en los ejercicios.

## Para el formador

Antes de impartir, prepara el entorno siguiendo [00-preparacion-demo-formador.md](00-preparacion-demo-formador.md). Ese documento lista modelos, knowledge bases, agentes, herramientas, evaluaciones y trazas que conviene dejar creados para evitar depender de cuotas o indexaciones en directo.

## Licencia y uso

Material elaborado por Intelequia para uso formativo. Puede reutilizarse internamente citando la fuente. Los datos y documentos sintéticos pueden modificarse y publicarse libremente.
