# Ejercicio 4 (Azure ML Studio) · Integración con Foundry y Fabric

**Tiempo estimado:** 45 min · **Modalidad:** casa / discusión en aula

## Objetivo

Diseñar una arquitectura donde Fabric aporta datos, Azure ML genera predicciones y Foundry consume esas predicciones en una experiencia de agente.

## Prerequisitos

- Conocer el flujo básico de Foundry Agent Service.
- Haber completado o revisado los ejercicios de Azure ML Studio.
- Tener claro el caso Aurora Energía.

## Escenario

Aurora Energía quiere priorizar incidencias operativas. El equipo de datos ya trabaja en Fabric y mantiene un lakehouse con incidencias históricas. El equipo de IA quiere entrenar un modelo predictivo en Azure ML y usar la predicción dentro de un agente Foundry para orientar al técnico de soporte.

## Pasos

1. Dibuja el flujo de datos:
   - Fabric Lakehouse o ADLS Gen2
   - Azure ML datastore/data asset
   - job o pipeline de entrenamiento
   - modelo registrado
   - endpoint online o batch
   - agente Foundry o dashboard Fabric
2. Decide quién es dueño de cada pieza:
   - datos fuente
   - features
   - modelo
   - endpoint
   - agente
   - monitorización
3. Define qué consume Foundry:
   - API online de Azure ML como tool
   - tabla de predicciones batch
   - documento o resumen generado desde Fabric
4. Lista controles mínimos:
   - identidad
   - permisos sobre datos
   - identidad manejada de Azure AI Search si Foundry indexa OneLake
   - permisos de Search sobre Fabric/OneLake
   - permisos de Foundry sobre Azure AI Search o la knowledge base
   - logs
   - coste
   - revisión humana
5. Escribe tres preguntas que el agente Foundry podría responder usando la predicción.

## Entregable

Diagrama simple y tabla de decisiones de plataforma.

## Validación

- [ ] Fabric queda como origen o destino de datos, no como sustituto de Azure ML.
- [ ] Azure ML queda como responsable de entrenamiento y despliegue predictivo.
- [ ] Foundry queda como experiencia de agente o aplicación generativa.
- [ ] El diseño incluye identidad, permisos y monitorización.
- [ ] Si Foundry consume OneLake con una knowledge base, el diseño incluye Search con identidad manejada y permisos explícitos.
