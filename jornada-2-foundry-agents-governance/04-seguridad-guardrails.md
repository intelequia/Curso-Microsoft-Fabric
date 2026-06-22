# J2-M4 · Seguridad, identidad, red privada y guardrails

**Duración:** 30 min · **Formato:** explicación + checklist

## Objetivos

1. Diseñar seguridad para agentes empresariales.
2. Entender identidad de agente, RBAC, managed identity y OBO.
3. Aplicar guardrails contra fugas, prompt injection y uso indebido.

## Contenido

La seguridad de un agente combina controles de plataforma, controles de datos y controles de comportamiento.

### Capas

| Capa | Controles |
| --- | --- |
| Identidad | Entra ID, RBAC, managed identities, OBO. |
| Red | Private endpoints, VNet, bloqueo de acceso público. |
| Datos | Azure AI Search con permisos, Storage, Cosmos DB, Purview. |
| Modelo | Content filters, safety policies, rechazo de datos sensibles. |
| Herramientas | Scope mínimo, allowlist, auditoría, rate limits. |
| Aplicación | Autorización por usuario, logging, revisión humana. |

## Riesgos habituales

- Prompt injection desde documentos.
- Herramientas con permisos excesivos.
- Respuestas sin citas.
- Indexar documentos sin ACL.
- Mezclar datos de tenants o áreas.
- Guardar conversaciones con información sensible sin retención definida.

## Mensajes clave

- El agente no debe tener más permisos que el usuario o proceso que representa.
- Las herramientas son superficie de ataque.
- La seguridad debe probarse con red teaming, no solo revisarse en arquitectura.
