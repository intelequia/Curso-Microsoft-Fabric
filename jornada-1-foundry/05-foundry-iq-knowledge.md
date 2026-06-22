# J1-M5 · Foundry IQ y knowledge bases

**Duración:** 30 min · **Formato:** explicación + demo

## Objetivos

1. Entender Foundry IQ como capa de conocimiento para agentes.
2. Crear una knowledge base con fuentes empresariales.
3. Conectar conocimiento a un agente o aplicación.

## Contenido

Foundry IQ permite crear knowledge bases reutilizables y permission-aware para que agentes y aplicaciones accedan a datos empresariales. Se apoya en Azure AI Search y puede conectar documentos, fuentes Azure, SharePoint, OneLake y web, según disponibilidad.

Cuando la fuente es Fabric OneLake, la seguridad no depende solo del usuario que crea la demo. La indexación la ejecuta Azure AI Search por debajo, por lo que el recurso de Search necesita identidad manejada habilitada y permisos de lectura sobre OneLake. Foundry, además, necesita permisos para usar el recurso de búsqueda o la conexión de la knowledge base.

### Relación con otros IQ

| Capa | Enfoque |
| --- | --- |
| **Foundry IQ** | Conocimiento empresarial para agentes en Foundry. |
| **Fabric IQ** | Semántica y razonamiento sobre datos analíticos en Microsoft Fabric. |
| **Work IQ** | Contexto de colaboración de Microsoft 365. |

### Flujo típico

1. Crear o conectar Azure AI Search.
2. Si se usa OneLake, habilitar identidad manejada en Azure AI Search.
3. Conceder permisos a Search sobre Fabric/OneLake y a Foundry sobre Search.
4. Añadir fuentes de conocimiento.
5. Configurar chunking, metadatos y retrieval.
6. Probar consultas.
7. Conectar la knowledge base a un agente.
8. Evaluar respuestas citadas.

### Identidad y permisos

| Pieza | Por qué importa |
| --- | --- |
| Azure AI Search con identidad manejada | Es quien indexa y consulta el contenido usado por la knowledge base. |
| Permisos de Search sobre OneLake | Permiten leer datos de Fabric sin credenciales personales ni claves compartidas. |
| Permisos de Foundry sobre Search | Permiten que el agente use la knowledge base durante la conversación. |

## Demo en vivo

1. Subir documentos de `assets/docs`.
2. Crear knowledge base `kb-aurora-operaciones`.
3. Si se conecta OneLake, revisar identidad manejada y permisos.
4. Probar preguntas:
   - "¿Cuál es el SLA para incidencias críticas?"
   - "¿Qué datos no puede revelar el asistente?"
5. Revisar citas y documentos usados.

## Mensajes clave

- Foundry IQ separa conocimiento reutilizable de un agente concreto.
- Azure AI Search sigue siendo una pieza central del retrieval.
- Para OneLake, Search necesita identidad manejada y permisos; Foundry necesita acceso al recurso de búsqueda.
- El éxito depende de permisos, metadatos, calidad documental y evaluación.
