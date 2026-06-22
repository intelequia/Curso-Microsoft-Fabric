# Ejercicio 3 (Jornada 1) · Knowledge base y evaluación básica

**Tiempo estimado:** 90 min · **Modalidad:** casa

## Objetivo

Crear una knowledge base con documentos de Aurora y evaluar respuestas básicas.

## Pasos

1. Crea o conecta un servicio Azure AI Search.
2. Si la fuente está en Fabric OneLake, habilita la identidad manejada del recurso Azure AI Search.
3. Concede permisos de lectura a la identidad de Azure AI Search sobre el workspace, lakehouse o carpeta de OneLake.
4. Concede a Foundry permisos para usar el recurso Azure AI Search o la conexión de la knowledge base.
5. En Foundry, crea `kb-aurora-operaciones`.
6. Añade los documentos de `assets/docs`.
7. Prueba estas preguntas:
   - "Cual es el SLA de una incidencia critica?"
   - "Que hago si falla un punto de recarga?"
   - "Que usos de IA estan prohibidos?"
8. Verifica que las respuestas citan fuentes.
9. Usa `assets/data/eval_questions.csv` como batería inicial.
10. Ejecuta una evaluación desde portal o SDK si está disponible en tu tenant.

## Entregable

Capturas de tres respuestas con citas y tabla con resultados de evaluación.

## Validación

- [ ] Knowledge base creada.
- [ ] Si se usa OneLake, Azure AI Search tiene identidad manejada habilitada.
- [ ] Search tiene permisos de lectura sobre Fabric/OneLake.
- [ ] Foundry tiene permisos sobre Azure AI Search o la knowledge base.
- [ ] Hay citas a documentos.
- [ ] Las preguntas de rechazo no inventan políticas ni revelan datos personales.
