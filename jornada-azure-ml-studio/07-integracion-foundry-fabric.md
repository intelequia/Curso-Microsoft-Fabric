# AML-M7 · Integración con Foundry y Fabric

**Duración:** 20 min · **Formato:** arquitectura + conversación

## Objetivos

1. Decidir cuándo usar Foundry, Azure ML Studio y Fabric en una misma solución.
2. Diseñar patrones de integración entre datos, modelos predictivos y agentes.
3. Identificar límites, responsabilidades y riesgos de cada plataforma.

## Hilo narrativo

> "La solución empresarial no vive en un portal. Fabric organiza datos, Azure ML produce modelos predictivos y Foundry convierte capacidades en experiencias de IA generativa y agentes."

## Contenido

### Patrón de referencia

```text
Fabric / ADLS Gen2
  -> preparación de datos y features
  -> Azure ML job / pipeline
  -> modelo registrado
  -> endpoint online o batch
  -> aplicación, informe o agente Foundry
```

### Decisiones de arquitectura

| Necesidad | Plataforma principal |
| --- | --- |
| Consultar datos analíticos, lakehouse o BI | Fabric |
| Preparar features y datasets de entrenamiento | Fabric o Azure ML, según ownership del dato |
| Entrenar y comparar modelos predictivos | Azure ML Studio |
| Registrar, desplegar y operar modelos ML | Azure ML Studio |
| Crear agente conversacional con tools y conocimiento | Microsoft Foundry |
| Usar predicción ML dentro de un agente | Foundry llamando a API/endpoint de Azure ML |
| Mostrar predicciones en informes | Fabric / Power BI |

### Identidad en OneLake y Foundry

Cuando Foundry usa una knowledge base sobre datos de Fabric/OneLake, la lectura no se hace con permisos implícitos del usuario. La ingesta se apoya en Azure AI Search:

```text
Foundry knowledge base
  -> Azure AI Search
  -> identidad manejada de Search
  -> Fabric OneLake
```

Por tanto, el diseño debe incluir:

| Paso | Control |
| --- | --- |
| Habilitar identidad manejada en Azure AI Search | Search puede autenticarse en Entra ID. |
| Conceder lectura a Search sobre OneLake | Search puede indexar los datos autorizados. |
| Conceder acceso a Foundry sobre Search/knowledge base | El agente puede usar la knowledge base en conversación. |
| Mantener permisos mínimos | El agente no debe heredar acceso amplio al lakehouse completo si no lo necesita. |

### Ejemplos Aurora

- Predicción de riesgo de incidencia por estación entrenada en Azure ML y consumida por un dashboard en Fabric.
- Endpoint de Azure ML que estima prioridad de ticket y se expone como tool para un agente Foundry.
- Batch scoring nocturno que escribe predicciones en lakehouse para análisis operativo.
- Knowledge base de Foundry que indexa procedimientos o datos publicados en OneLake mediante Azure AI Search con identidad manejada.

## Demo en vivo

1. Mostrar el diagrama de referencia.
2. Revisar cómo un endpoint de Azure ML podría exponerse como API para Foundry.
3. Revisar cómo un batch endpoint puede escribir predicciones para Fabric.
4. Revisar el patrón de permisos para OneLake: Search con identidad manejada y Foundry con acceso al Search.
5. Cerrar con criterios de decisión por caso de uso.

## Mensajes clave

- Foundry, Azure ML y Fabric son complementarios.
- La frontera debe definirse por responsabilidad: datos, modelos predictivos, agentes y experiencia de usuario.
- La integración debe respetar identidad, permisos, linaje y coste.
- En OneLake, no basta con permisos del usuario: los servicios que indexan o consultan datos necesitan identidad y permisos explícitos.
