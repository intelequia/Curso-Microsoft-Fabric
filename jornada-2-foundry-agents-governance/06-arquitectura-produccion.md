# J2-M6 · Arquitectura de producción

**Duración:** 30 min · **Formato:** explicación arquitectónica

## Objetivos

1. Diseñar una arquitectura empresarial para chat/agentes con Foundry.
2. Identificar componentes Azure necesarios.
3. Separar prototipo, piloto y producción.

## Arquitectura base

```text
Usuarios
  |
Web / Teams / Copilot
  |
App Service / API Management
  |
Foundry Agent Service
  |------ Azure AI Search (knowledge)
  |------ Azure Storage (archivos)
  |------ Cosmos DB (estado y conversaciones)
  |------ Application Insights (trazas)
  |------ APIs internas / MCP / OpenAPI
```

En producción, el patrón recomendado incluye autenticación Entra ID, private endpoints, recursos dedicados para estado, trazas, datos y búsqueda, y separación por entorno.

## Decisiones clave

| Decisión | Recomendación |
| --- | --- |
| Entornos | Dev, test y prod separados. |
| Identidad | Managed identity y OBO cuando aplique. |
| Red | Bloquear público si hay datos sensibles. |
| Estado | Cosmos DB o recurso gestionado según setup de Agent Service. |
| Documentos | Storage con retención y auditoría. |
| Observabilidad | Application Insights y alertas. |
| Evaluación | Gate de calidad antes de publicar. |

## Mensajes clave

- Una demo de portal no es una arquitectura de producción.
- BYO resources aporta control de residencia, auditoría y retención.
- La arquitectura debe incluir operación y gobierno desde el día uno.
